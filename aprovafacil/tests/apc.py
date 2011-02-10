# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

from decimal import Decimal
import time

from aprovafacil.wrapper import AprovaFacilWrapper

class TestAPC(TestCase):

    def setUp(self):
      self.url = 'http://localhost/cgi-bin/CGIAprovaFacil'

    def get_post_data(self, **kwargs):
        post_data = {
            'NumeroDocumento': '1',
            'ValorDocumento': '101.75',
            'QuantidadeParcelas': 1,
            'NumeroCartao': '5555666677778884', # Cartao teste mastercard
            'MesValidade': '12',
            'AnoValidade': time.strftime('%y', time.localtime()),
            'CodigoSeguranca': '111',
            'EnderecoIPComprador': '10.0.0.1',
            'NomePortadorCartao': '',
            'Bandeira': '',
            'CPFPortadorCartao': '',
        }
        post_data.update(**kwargs)
        return post_data

    def test_sucesso_autorizacao(self):
        pass

    def test_autorizacao_sem_endereco_ip_funciona(self):
        pass

    def test_autorizacao_sem_nome_portador_funciona(self):
        pass

    def test_autorizacao_sem_bandeira_funciona(self):
        pass

    def test_autorizacao_sem_cpf_funciona(self):
        pass

    def test_transacao_com_valor_float_funciona(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(ValorDocumento=1.1)

    def test_quantidade_parcelas_pode_ser_omitida(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(QuantidadeParcelas=None)
        wrapper.do_apc(**post_data)

    ###

    def test_quantidade_parcelas_negativa_gera_falha(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(QuantidadeParcelas=-3)
        self.assertRaises(ValueError, wrapper.do_apc, **post_data)

    def test_autorizacao_sem_numero_documento_falha(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(NumeroDocumento=None)
        self.assertRaises(ValueError, wrapper.do_apc, **post_data)

    def test_autorizacao_sem_valor_falha(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(ValorDocumento=None)
        self.assertRaises(ValueError, wrapper.do_apc, **post_data)

    def test_transacao_com_valor_de_tipo_invalido_falha(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(ValorDocumento='NoNumber')
        self.assertRaises(ValueError, wrapper.do_apc, **post_data)

    def test_transacao_sem_numero_cartao_falha(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(NumeroCartao=None)
        self.assertRaises(ValueError, wrapper.do_apc, **post_data)

    def test_transacao_sem_mes_validade_cartao_falha(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(MesValidade=None)
        self.assertRaises(ValueError, wrapper.do_apc, **post_data)

    def test_transacao_sem_ano_validade_cartao_falha(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(AnoValidade=None)
        self.assertRaises(ValueError, wrapper.do_apc, **post_data)

    def test_transacao_sem_codigo_cartao_falha(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CodigoSeguranca=None)
        self.assertRaises(ValueError, wrapper.do_apc, **post_data)

    def test_transacao_sem_ip_comprador_falha(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(EnderecoIPComprador=None)
        self.assertRaises(ValueError, wrapper.do_apc, **post_data)

    def test_endereco_ip_comprador_malformado_gera_falha(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(EnderecoIPComprador='NoIP')
        self.assertRaises(ValueError, wrapper.do_apc, **post_data)

    def test_endereco_ip_nao_pode_ser_localhost(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(EnderecoIPComprador='127.0.0.2')
        self.assertRaises(ValueError, wrapper.do_apc, **post_data)

    def test_transacao_com_cartao_expirado_falha(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(AnoValidade='88')
        self.assertRaises(ValueError, wrapper.do_apc, **post_data)
