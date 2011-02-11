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


    def __init__(self, cgi_url, **kwargs):
        self.cgi_url = cgi_url
        self.request_data = kwargs
        self._errors = {}


    @property
    def errors(self):
        if not self._errors:
            self.validate()
        return self._errors


    def validate(self):
        pre_validate = getattr(self, 'pre_validate', None)
        pos_validate = getattr(self, 'pos_validate', None)

        if pre_validate:
            pre_validate()

        for field in self.mandatory_fields:
            if self.request_data.get(field, None) is None:
                self._errors[field] = "Required field '%s'"

        if pos_validate:
            pos_validate()


    def make_request(self):
        # Validate the request data
        if self.errors:
            raise ValueError('Errors in request data. (%s)' % ', '.join(self.errors.keys()))

        http = httplib2.Http()
        response, content = http.request(
            self.url, 'POST',
            body=urlencode(self.request_data),
            headers = {'cache-control': 'no-cache'},
        )

        return self.parse_response(response, content)


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


    def pre_validate(self):
        self.validate_QuantidadeParcelas()


    def pos_validate(self):
        request_data = self.request_data
        if 'TransacaoAnterior' in request_data:
            # Recurring charge mandatory fields are different
            self.mandatory_fields = self.recurring_charge_fields
        else:
            # First charge
            self.validate_CreditCardExpiration()
            self.validate_EnderecoIPComprador()

        self.validate_ValorDocumento()


    def validate_QuantidadeParcelas(self):
        if 'QuantidadeParcelas' in self._errors:
            return

        request_data = self.request_data

        parcels = request_data.get('QuantidadeParcelas', None)
        if parcels is None:
            request_data['QuantidadeParcelas'] = 1
        else:
            try:
                if int(parcels) < 1:
                    raise ValueError
            except ValueError:
                self._errors["QuantidadeParcelas"] = "QuantidadeParcelas must be >= 1"


    def validate_ValorDocumento(self):
        if 'ValorDocumento' in self._errors:
            return

        request_data = self.request_data
        try:
            input_value = request_data['ValorDocumento']
            if isinstance(input_value, float):
                input_value = str(input_value)
            decimal_value = Decimal(input_value)

        except (TypeError, decimal.InvalidOperation):
            msg = 'Invalid Document Value (%s)' % request_data['ValorDocumento']
            self._errors['ValorDocumento'] = msg


    def validate_CreditCardExpiration(self):
        if 'MesValidade' in self._errors or 'AnoValidade' in self._errors:
            return

        request_data = self.request_data

        expiracao_cartao = time.strptime(
            "%(AnoValidade)s/%(MesValidade)s" % request_data,
            "%y/%m"
        )
        if not expiracao_cartao > time.localtime():
            msg = "Cartao expirado em %(MesValidade)s/%(AnoValidade)s" % request_data
            self._errors['MesValidade'] = msg
            self._errors['AnoValidade'] = msg


    def validate_EnderecoIPComprador(self):
        if 'EnderecoIPComprador' in self._errors:
            return

        request_data = self.request_data
        try:
            client_ip = IP(request_data['EnderecoIPComprador'])
        except ValueError:
            self._errors['EnderecoIPComprador'] = 'Invalid IP address'
            return

        localnet = IP('127.0.0.0/30')
        if client_ip in localnet:
            self._errors['EnderecoIPComprador'] = 'Localhost addresses are not accepted'
            return


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

    mandatory_fields = ('NumeroDocumento', 'Transacao')


    def __init__(self, *args, **kwargs):
        super(CAP, self).__init__(*args, **kwargs)
        self.url = '%s/CAP' % self.cgi_url

    def parse_response(self, response, content):
        status = int(response['status'])
        if status == 200:
            result = xmltodict(content)
        else:
            result = {}

        return result


class CAN(AprovaFacilWrapper):

    mandatory_fields = ('NumeroDocumento', 'Transacao')


    def __init__(self, *args, **kwargs):
        super(CAN, self).__init__(*args, **kwargs)
        self.url = '%s/CAN' % self.cgi_url

    def parse_response(self, response, content):
        status = int(response['status'])
        if status == 200:
            result = xmltodict(content)
        else:
            result = {}

        return result
