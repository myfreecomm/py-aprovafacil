# -*- coding: utf-8 -*-
import time
from datetime import date
from urllib import urlencode
from abc import ABCMeta, abstractmethod

import decimal
from decimal import Decimal
import httplib
import httplib2
from IPy import IP

from utils import xmltodict
from exceptions import RemoteServerException, InvalidLicense


__all__ = ['AprovaFacilWrapper', ]


class AprovaFacilWrapper(object):

    __metaclass__ = ABCMeta

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
        try:
            response, content = http.request(
                self.url, 'POST',
                body=urlencode(self.request_data),
                headers = {'cache-control': 'no-cache'},
            )
        except AttributeError:
            # See http://code.google.com/p/httplib2/issues/detail?id=96
            raise httplib.HTTPException()

        return self.parse_response(response, content)


    def parse_response(self, response, content):
        status = int(response['status'])
        if status == 200:
            result = xmltodict(content)
            if result:
                return self.parse_response_content(result)

            else:
                # XML de formato inesperado
                raise InvalidLicense('CGI error. Check licence file')

        else:
            raise RemoteServerException('HTTP Error, status %d' % status)


    @abstractmethod
    def parse_response_content(self, result):
        pass


class APC(AprovaFacilWrapper):

    mandatory_fields = (
        'NumeroDocumento', 'ValorDocumento', 'QuantidadeParcelas',
        'NumeroCartao', 'MesValidade', 'AnoValidade', 'CodigoSeguranca',
    )

    recurring_charge_fields = (
        'Transacao', 'ValorDocumento', 'QuantidadeParcelas'
    )


    def __init__(self, *args, **kwargs):
        super(APC, self).__init__(*args, **kwargs)
        self.url = '%s/APC' % self.cgi_url


    def pre_validate(self):
        if 'Transacao' in self.request_data:
            # Recurring charge mandatory fields are different
            self.mandatory_fields = self.recurring_charge_fields
        self.validate_QuantidadeParcelas()


    def pos_validate(self):
        request_data = self.request_data
        if 'Transacao' not in request_data:
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

        try:
            today = date.today()
            expiracao_cartao = date(
                *time.strptime('%(MesValidade)s/%(AnoValidade)s' % request_data,
                '%m/%y'
            )[:3])

            if expiracao_cartao < date(today.year, today.month, 1):
                msg = "Cartao expirado em %(MesValidade)s/%(AnoValidade)s" % request_data
                self._errors['MesValidade'] = msg
                self._errors['AnoValidade'] = msg

        except ValueError:
            msg = 'Both AnoValidade and MesValidade should be composed of 1 or 2 digits'
            self._errors['MesValidade'] = msg
            self._errors['AnoValidade'] = msg


    def validate_EnderecoIPComprador(self):
        if 'EnderecoIPComprador' in self._errors:
            return

        EnderecoIPComprador = self.request_data.get('EnderecoIPComprador', None)

        if EnderecoIPComprador is not None:
            try:
                client_ip = IP(EnderecoIPComprador)
            except ValueError:
                self._errors['EnderecoIPComprador'] = 'Invalid IP address'
                return

            localnet = IP('127.0.0.0/30')
            if client_ip in localnet:
                self._errors['EnderecoIPComprador'] = 'Localhost addresses are not accepted'
                return


    def parse_response_content(self, result):
        approved_string = result.get('TransacaoAprovada', None)
        result['approved'] = (approved_string == 'True')
        result['failure_reason'] = self.get_failure_reason(result)
        return result


    def get_failure_reason(self, result):
        if not result['approved']:
            try:
                return result['ResultadoSolicitacaoAprovacao']

            except IndexError:
                return None

        else:
            return None


class CanCapWrapper(AprovaFacilWrapper):

    # 'NumeroDocumento' is an optional field
    mandatory_fields = ('Transacao', )
    url_suffix = 'NotSet'

    def __init__(self, *args, **kwargs):
        super(CanCapWrapper, self).__init__(*args, **kwargs)
        self.url = '%s/%s' % (self.cgi_url, self.url_suffix)


    def parse_response_content(self, result):
        approved_string = result.get('ResultadoSolicitacaoAprovacao', None)
        result['approved'] = (approved_string.startswith('Confirmado'))
        result['failure_reason'] = self.get_failure_reason(result)
        return result


    def get_failure_reason(self, result):
        if not result['approved']:
            return result['ResultadoSolicitacaoAprovacao']
        else:
            return None


class CAN(CanCapWrapper):

    url_suffix = 'CAN'

    def __init__(self, *args, **kwargs):
        super(CAN, self).__init__(*args, **kwargs)
        raise NotImplementedError


class CAP(CanCapWrapper):

    url_suffix = 'CAP'
