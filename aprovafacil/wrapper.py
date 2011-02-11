# -*- coding: utf-8 -*-
import time
from urllib import urlencode

import decimal
from decimal import Decimal

import httplib2
from IPy import IP

from utils import xmltodict

class AprovaFacilWrapper(object):

    FAILURE_REASONS = {
        '30': 'Random',
        '78': 'Blocked credit card',
        '14': 'Invalid credit card',
        '54': 'Expired credit card',
        'N7': 'Invalid security code',
        '84': 'Please retry',
        '68': 'Duplicated transaction',
        '60': 'Invalid amount',
        '56': 'Invalid data',
    }


    def __init__(self, cgi_url, validate_request=True):
        self.cgi_url = cgi_url
        self.validate_request = validate_request

    def validate(self, request_data):
        if 'TransacaoAnterior' in request_data:
            # Recurring charge
            self.validate_recurring_charge_input(request_data)
        else:
            # First charge
            self.validate_first_charge_input(request_data)
            self.validate_cc_expiration(request_data)
            self.validate_ip_address(request_data)

        self.validate_transaction_value(request_data)

    def validate_recurring_charge_input(self, request_data):
        apc_parameters = (
            'TransacaoAnterior', 'ValorDocumento', 'QuantidadeParcelas'
        )

        parcels = request_data.get('QuantidadeParcelas', None)
        if parcels is None:
            request_data['QuantidadeParcelas'] = 1
        else:
            try:
                parcels = int(parcels)
            except ValueError:
                raise ValueError("QuantidadeParcelas must be >= 1")

            if parcels < 1:
                raise ValueError("QuantidadeParcelas must be >= 1")

        for key in apc_parameters:
            if request_data.get(key, None) is None:
                raise ValueError("Parameter '%s' is required" % key)

    def validate_first_charge_input(self, request_data):
        apc_parameters = (
            'NumeroDocumento', 'ValorDocumento', 'QuantidadeParcelas',
            'NumeroCartao', 'MesValidade', 'AnoValidade', 'CodigoSeguranca',
            'EnderecoIPComprador',
        )

        parcels = request_data.get('QuantidadeParcelas', None)
        if parcels is None:
            request_data['QuantidadeParcelas'] = 1
        else:
            try:
                parcels = int(parcels)
            except ValueError:
                raise ValueError("QuantidadeParcelas must be >= 1")

            if parcels < 1:
                raise ValueError("QuantidadeParcelas must be >= 1")

        for key in apc_parameters:
            if request_data.get(key, None) is None:
                raise ValueError("Parameter '%s' is required" % key)

    def validate_cc_expiration(self, request_data):
        expiracao_cartao = time.strptime(
            "%(AnoValidade)s/%(MesValidade)s" % request_data,
            "%y/%m"
        )
        if not expiracao_cartao > time.localtime():
            msg = "Cartao expirado em %(MesValidade)s/%(AnoValidade)s"
            raise ValueError(msg % request_data)

    def validate_transaction_value(self, request_data):
        try:
            input_value = request_data['ValorDocumento']
            if isinstance(input_value, float):
                input_value = str(input_value)
            decimal_value = Decimal(input_value)
        except decimal.InvalidOperation:
            msg = 'Invalid Document Value (%s)'
            raise ValueError(msg % request_data['ValorDocumento'])

    def validate_ip_address(self, request_data):
        try:
            client_ip = IP(request_data['EnderecoIPComprador'])
        except ValueError:
            raise ValueError('Invalid IP address')

        localnet = IP('127.0.0.0/30')
        if client_ip in localnet:
            raise ValueError('Localhost addresses are not accepted')

    def get_failure_reason(self, result):
        if not result['approved']:
            try:
                code =  result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip()
            except IndexError:
                code = None

            return AprovaFacilWrapper.FAILURE_REASONS.get(code, 'Unknown')
        else:
            return None

    def do_apc(self, *args, **kwargs):
        request_data = kwargs

        # Validate the request data
        if self.validate_request:
            self.validate(request_data)

        # Make the request
        apc_url = '%s/APC' % self.cgi_url

        http = httplib2.Http()
        response, content = http.request(
            apc_url, 'POST',
            body=urlencode(request_data),
            headers = {'cache-control': 'no-cache'},
        )

        status = int(response['status'])
        if status == 200:
            result = xmltodict(content)
            approved_string = result.get('TransacaoAprovada', None)
            if approved_string is None:
                # XML de formato inesperado
                result['approved'] = False
                result['failure_reason'] = 'CGI error. Check licence file'
            else:
                result['approved'] = (approved_string == 'True')
                result['failure_reason'] = self.get_failure_reason(result)

        else:
            result = {
                'approved': False,
                'failure_reason': 'HTTP Error, status %d' % status,
            }

        return result
