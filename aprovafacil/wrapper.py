# -*- coding: utf-8 -*-
import time
import decimal
from decimal import Decimal
from IPy import IP

class AprovaFacilWrapper(object):

    def __init__(self, validate_request=True):
        self.validate_request = validate_request

    def validate_apc_input(self, request_data):
        apc_parameters = (
            'NumeroDocumento', 'ValorDocumento', 'NumeroCartao',
            'MesValidade', 'AnoValidade', 'CodigoSeguranca',
            'EnderecoIPComprador',
        )

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

    def do_apc(self, *args, **kwargs):
        request_data = kwargs

        if self.validate_request:
            self.validate_apc_input(request_data)
            self.validate_cc_expiration(request_data)
            self.validate_transaction_value(request_data)
            self.validate_ip_address(request_data)
