# -*- coding: utf-8 -*-
import time
from urllib import urlencode

import decimal
from decimal import Decimal

import httplib2
from IPy import IP

from utils import xmltodict

class AprovaFacilWrapper(object):

    def __init__(self, cgi_url, validate_request=True):
        self.cgi_url = cgi_url
        self.validate_request = validate_request

    def validate_apc_input(self, request_data):
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

        if request_data.get('QuantidadeParcelas', None) is None:
            request_data['QuantidadeParcelas'] = 1

        if 'QuantidadeParcelas' not in request_data:
            request_data['QuantidadeParcelas'] = 1

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

    def do_apc(self, *args, **kwargs):
        request_data = kwargs

        # Validate the request data
        if self.validate_request:
            self.validate_apc_input(request_data)
            self.validate_cc_expiration(request_data)
            self.validate_transaction_value(request_data)
            self.validate_ip_address(request_data)

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
        else:
            result = None

        return status, result