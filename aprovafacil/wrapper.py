# -*- coding: utf-8 -*-
import time
from urllib import urlencode

import decimal
from decimal import Decimal

import httplib2
from IPy import IP

from utils import xmltodict

__all__ = ['AprovaFacilWrapper', ]


class AprovaFacilWrapper(object):

    mandatory_fields = ()
    _errors = {}


    def __init__(self, cgi_url, **kwargs):
        self.cgi_url = cgi_url
        self.request_data = kwargs


    @property
    def errors(self):
        if not self._errors:
            self._errors = self.validate()
        return self.errors


    def validate(self):
        errors = {}

        extra_validation = getattr(self, 'extra_validation', None)
        if extra_validation:
            errors.update(extra_validation())

        for field in self.mandatory_fields:
            if request_data.get(field, None) is None:
                errors[field] = "Required field '%s'"

        return errors


    def make_request(self):
        # Validate the request data
        if self.errors:
            raise ValueError('Errors in request data.')

        http = httplib2.Http()
        response, content = http.request(
            self.url, 'POST',
            body=urlencode(seld.request_data),
            headers = {'cache-control': 'no-cache'},
        )

        self.parse_response(response, content)


class APC(AprovaFacilWrapper):

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

    mandatory_fields = (
        'NumeroDocumento', 'ValorDocumento', 'QuantidadeParcelas',
        'NumeroCartao', 'MesValidade', 'AnoValidade', 'CodigoSeguranca',
        'EnderecoIPComprador',
    )

    recurring_charge_fields = (
        'TransacaoAnterior', 'ValorDocumento', 'QuantidadeParcelas'
    )


    def __init__(self, *args, **kwargs):
        super(APC, self).__init__(*args, **kwargs)
        self.url = '%s/APC' % self.cgi_url


    def extra_validation(self):
        request_data = self.request_data
        if 'TransacaoAnterior' in request_data:
            # Recurring charge mandatory fields are different
            self.mandatory_fields = self.recurring_charge_fields
        else:
            # First charge
            self.errors.update(self.validate_CreditCardExpiration())
            self.errors.update(self.validate_EnderecoIPComprador())

        self.errors.update(self.validate_QuantidadeParcelas())
        self.errors.update(self.validate_ValorDocumento())

        return self.errors


    def validate_QuantidadeParcelas(self):
        request_data = self.request_data
        errors = {}

        parcels = request_data.get('QuantidadeParcelas', None)
        if parcels is None:
            request_data['QuantidadeParcelas'] = 1
        else:
            try:
                if int(parcels) < 1:
                    raise ValueError
            except ValueError:
                errors["QuantidadeParcelas"] = "QuantidadeParcelas must be >= 1"

        return errors


    def validate_ValorDocumento(self, request_data):
        try:
            input_value = request_data['ValorDocumento']
            if isinstance(input_value, float):
                input_value = str(input_value)
            decimal_value = Decimal(input_value)
            return {}

        except decimal.InvalidOperation:
            msg = 'Invalid Document Value (%s)' % request_data['ValorDocumento']
            return {'ValorDocumento': msg}


    def validate_CreditCardExpiration(self):
        request_data = self.request_data

        expiracao_cartao = time.strptime(
            "%(AnoValidade)s/%(MesValidade)s" % request_data,
            "%y/%m"
        )
        if not expiracao_cartao > time.localtime():
            msg = "Cartao expirado em %(MesValidade)s/%(AnoValidade)s" % request_data
            return {'MesValidade': msg, 'AnoValidade': msg}
        else:
            return {}


    def validate_EnderecoIPComprador(self, request_data):
        errors = {}

        try:
            client_ip = IP(request_data['EnderecoIPComprador'])
        except ValueError:
            errors['EnderecoIPComprador'] = 'Invalid IP address'

        localnet = IP('127.0.0.0/30')
        if client_ip in localnet:
            errors['EnderecoIPComprador'] = 'Localhost addresses are not accepted'

        return errors


    def parse_response(self, response, content):
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


    def get_failure_reason(self, result):
        if not result['approved']:
            try:
                code =  result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip()
            except IndexError:
                code = None

            return APC.FAILURE_REASONS.get(code, 'Unknown')
        else:
            return None


class CAP(AprovaFacilWrapper):

    def do_cap(self, *args, **kwargs):
        request_data = kwargs

        # Validate the request data
        self.validate_cap_can(request_data)

        # Make the request
        apc_url = '%s/CAP' % self.cgi_url

        response, content = self._make_request(apc_url, request_data)


class CAN(AprovaFacilWrapper):

    def do_can(self, *args, **kwargs):
        request_data = kwargs

        # Validate the request data
        self.validate_cap_can(request_data)

        # Make the request
        apc_url = '%s/CAN' % self.cgi_url

        response, content = self._make_request(apc_url, request_data)
