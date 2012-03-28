# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from mock import Mock, patch
import time
from datetime import date
from decimal import Decimal
from httplib2 import Http

from aprovafacil.wrapper import APC
from aprovafacil.exceptions import RemoteServerException, InvalidLicense
import mocked_responses

__all__ = [
    'TestFirstCharge', 'TestFirstChargeValidation',
    'TestRecurringCharge', 'TestRecurringChargeValidation',
]

http_200 = {'status': '200'}
http_500 = {'status': '500'}

http_error = (http_500, '')
invalid_licence = (http_200, mocked_responses.invalid_licence)
accepted = (http_200, mocked_responses.accepted)
refused = (http_200, mocked_responses.refused)
blocked_credit_card = (http_200, mocked_responses.blocked_credit_card)
invalid_credit_card = (http_200, mocked_responses.invalid_credit_card)
expired_credit_card = (http_200, mocked_responses.expired_credit_card)
invalid_security_code = (http_200, mocked_responses.invalid_security_code)
invalid_amount = (http_200, mocked_responses.invalid_amount)
duplicated_transaction = (http_200, mocked_responses.duplicated_transaction)
invalid_data = (http_200, mocked_responses.invalid_data)
retry_transaction = (http_200, mocked_responses.retry_transaction)

##
# First Charge
##

class BaseAPCTest(TestCase):

    def setUp(self):
      self.url = 'http://localhost/cgi-bin/CGIAprovaFacil'


class BaseFirstChargeTest(BaseAPCTest):

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


class TestFirstCharge(BaseFirstChargeTest):

    @patch.object(Http, 'request', Mock(return_value=http_error))
    def test_erro_http(self):
        post_data = self.get_post_data()
        wrapper = APC(cgi_url=self.url, **post_data)
        self.assertRaises(RemoteServerException, wrapper.make_request)


    @patch.object(Http, 'request', Mock(return_value=invalid_licence))
    def test_arquivo_licenca_invalido(self):
        post_data = self.get_post_data(CodigoSeguranca=555)
        wrapper = APC(cgi_url=self.url, **post_data)
        self.assertRaises(InvalidLicense, wrapper.make_request)


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_autorizacao_aprovada(self):
        post_data = self.get_post_data(CodigoSeguranca=555)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=refused))
    def test_autorizacao_recusada(self):
        post_data = self.get_post_data(CodigoSeguranca=501)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - 30 - 30ALEATORIO')
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=blocked_credit_card))
    def test_autorizacao_recusada_cartao_bloqueado(self):
        post_data = self.get_post_data(CodigoSeguranca=502)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - 78 - 78CAR BLOQ1.USO')


    @patch.object(Http, 'request', Mock(return_value=invalid_credit_card))
    def test_autorizacao_recusada_cartao_invalido(self):
        post_data = self.get_post_data(CodigoSeguranca=504)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - 14 - 14CARTAOINVALIDO')


    @patch.object(Http, 'request', Mock(return_value=invalid_amount))
    def test_autorizacao_recusada_valor_invalido(self):
        post_data = self.get_post_data(CodigoSeguranca=506)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'],
            u'N?o Autorizado - 60 - Valor Inv?lido. Por favor, ent')


    @patch.object(Http, 'request', Mock(return_value=duplicated_transaction))
    def test_autorizacao_recusada_transacao_ja_efetuada(self):
        post_data = self.get_post_data(CodigoSeguranca=507)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - 68 - T68TRANSACAO JA EFETUADA')


    @patch.object(Http, 'request', Mock(return_value=expired_credit_card))
    def test_autorizacao_recusada_cartao_vencido(self):
        post_data = self.get_post_data(CodigoSeguranca=508)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - 54 - 54CARTAO VENCIDO')


    @patch.object(Http, 'request', Mock(return_value=invalid_data))
    def test_autorizacao_recusada_dados_invalidos(self):
        post_data = self.get_post_data(CodigoSeguranca=509)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'],
            u'N?o Autorizado - 56 - Dado Inv?lido. Por favor, entr')


    @patch.object(Http, 'request', Mock(return_value=invalid_security_code))
    def test_autorizacao_recusada_codigo_seguranca_invalido(self):
        post_data = self.get_post_data(CodigoSeguranca=444)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - N7 - N7COD.SEG.INVAL')


    @patch.object(Http, 'request', Mock(return_value=retry_transaction))
    def test_autorizacao_recusada_refaca_transacao(self):
        post_data = self.get_post_data(CodigoSeguranca=333)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - 84 - T84REFACA TRANS')


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_autorizacao_sem_nome_portador_funciona(self):
        post_data = self.get_post_data(NomePortadorCartao=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_autorizacao_sem_bandeira_funciona(self):
        post_data = self.get_post_data(Bandeira=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_autorizacao_sem_cpf_funciona(self):
        post_data = self.get_post_data(CPFPortadorCartao=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_transacao_com_valor_float_funciona(self):
        post_data = self.get_post_data(ValorDocumento=1.1)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_quantidade_parcelas_pode_ser_omitida(self):
        post_data = self.get_post_data(QuantidadeParcelas=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_extra_data_in_post_is_ignored(self):
        post_data = self.get_post_data(NaoFazDiferenca='sim', QuebraPost=False)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


class TestFirstChargeValidation(BaseFirstChargeTest):

    def test_quantidade_parcelas_negativa_gera_falha(self):
        post_data = self.get_post_data(QuantidadeParcelas=-3)
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('QuantidadeParcelas' in wrapper.errors)


    def test_autorizacao_sem_numero_documento_falha(self):
        post_data = self.get_post_data(NumeroDocumento=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('NumeroDocumento' in wrapper.errors)


    def test_autorizacao_sem_valor_falha(self):
        post_data = self.get_post_data(ValorDocumento=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('ValorDocumento' in wrapper.errors)


    def test_transacao_com_valor_de_tipo_invalido_falha(self):
        post_data = self.get_post_data(ValorDocumento='NoNumber')
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('ValorDocumento' in wrapper.errors)


    def test_transacao_sem_numero_cartao_falha(self):
        post_data = self.get_post_data(NumeroCartao=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('NumeroCartao' in wrapper.errors)


    def test_transacao_sem_mes_validade_cartao_falha(self):
        post_data = self.get_post_data(MesValidade=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('MesValidade' in wrapper.errors)


    def test_transacao_sem_ano_validade_cartao_falha(self):
        post_data = self.get_post_data(AnoValidade=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('AnoValidade' in wrapper.errors)


    def test_ano_validade_com_4_digitos_gera_falha(self):
        post_data = self.get_post_data(AnoValidade=time.strftime('%Y', time.localtime()))
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('AnoValidade' in wrapper.errors)


    def test_transacao_sem_codigo_cartao_falha(self):
        post_data = self.get_post_data(CodigoSeguranca=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('CodigoSeguranca' in wrapper.errors)


    def test_endereco_ip_comprador_malformado_gera_falha(self):
        post_data = self.get_post_data(EnderecoIPComprador='NoIP')
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('EnderecoIPComprador' in wrapper.errors)


    def test_endereco_ip_nao_pode_ser_localhost(self):
        post_data = self.get_post_data(EnderecoIPComprador='127.0.0.2')
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('EnderecoIPComprador' in wrapper.errors)


    def test_endereco_ip_nao_eh_adicionado_pela_validacao(self):
        post_data = self.get_post_data()
        del(post_data['EnderecoIPComprador'])
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertFalse('EnderecoIPComprador' in wrapper.errors)
        self.assertFalse('EnderecoIPComprador' in wrapper.request_data)


    def test_transacao_com_cartao_expirado_falha(self):
        post_data = self.get_post_data(AnoValidade='88')
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('AnoValidade' in wrapper.errors)
        self.assertTrue('MesValidade' in wrapper.errors)


    def test_transacao_com_cartao_no_ultimo_mes_de_validade_funciona(self):
        today = date.today()
        post_data = self.get_post_data(
            AnoValidade=today.year, MesValidade=today.month
        )
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('AnoValidade' in wrapper.errors)
        self.assertTrue('MesValidade' in wrapper.errors)


##
# Recurring Charge
##

class BaseRecurringChargeTest(BaseAPCTest):

    def get_post_data(self, **kwargs):
        post_data = {
            'Transacao': '73417867510462',
            'ValorDocumento': '101.75',
            'QuantidadeParcelas': 1,
        }
        post_data.update(**kwargs)
        return post_data


class TestRecurringCharge(BaseFirstChargeTest):

    @patch.object(Http, 'request', Mock(return_value=http_error))
    def test_erro_http(self):
        post_data = self.get_post_data()
        wrapper = APC(cgi_url=self.url, **post_data)
        self.assertRaises(RemoteServerException, wrapper.make_request)


    @patch.object(Http, 'request', Mock(return_value=invalid_licence))
    def test_arquivo_licenca_invalido(self):
        post_data = self.get_post_data(CodigoSeguranca=555)
        wrapper = APC(cgi_url=self.url, **post_data)
        self.assertRaises(InvalidLicense, wrapper.make_request)


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_autorizacao_aprovada(self):
        post_data = self.get_post_data(CodigoSeguranca=555)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=refused))
    def test_autorizacao_recusada(self):
        post_data = self.get_post_data(CodigoSeguranca=501)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - 30 - 30ALEATORIO')
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=blocked_credit_card))
    def test_autorizacao_recusada_cartao_bloqueado(self):
        post_data = self.get_post_data(CodigoSeguranca=502)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - 78 - 78CAR BLOQ1.USO')


    @patch.object(Http, 'request', Mock(return_value=invalid_credit_card))
    def test_autorizacao_recusada_cartao_invalido(self):
        post_data = self.get_post_data(CodigoSeguranca=504)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - 14 - 14CARTAOINVALIDO')


    @patch.object(Http, 'request', Mock(return_value=invalid_amount))
    def test_autorizacao_recusada_valor_invalido(self):
        post_data = self.get_post_data(CodigoSeguranca=506)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'],
            u'N?o Autorizado - 60 - Valor Inv?lido. Por favor, ent')


    @patch.object(Http, 'request', Mock(return_value=duplicated_transaction))
    def test_autorizacao_recusada_transacao_ja_efetuada(self):
        post_data = self.get_post_data(CodigoSeguranca=507)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'],
            u'N?o Autorizado - 68 - T68TRANSACAO JA EFETUADA')


    @patch.object(Http, 'request', Mock(return_value=expired_credit_card))
    def test_autorizacao_recusada_cartao_vencido(self):
        post_data = self.get_post_data(CodigoSeguranca=508)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - 54 - 54CARTAO VENCIDO')


    @patch.object(Http, 'request', Mock(return_value=invalid_data))
    def test_autorizacao_recusada_dados_invalidos(self):
        post_data = self.get_post_data(CodigoSeguranca=509)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'],
            u'N?o Autorizado - 56 - Dado Inv?lido. Por favor, entr')


    @patch.object(Http, 'request', Mock(return_value=invalid_security_code))
    def test_autorizacao_recusada_codigo_seguranca_invalido(self):
        post_data = self.get_post_data(CodigoSeguranca=444)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - N7 - N7COD.SEG.INVAL')


    @patch.object(Http, 'request', Mock(return_value=retry_transaction))
    def test_autorizacao_recusada_refaca_transacao(self):
        post_data = self.get_post_data(CodigoSeguranca=333)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], u'N?o Autorizado - 84 - T84REFACA TRANS')


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_autorizacao_sem_nome_portador_funciona(self):
        post_data = self.get_post_data(NomePortadorCartao=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_autorizacao_sem_bandeira_funciona(self):
        post_data = self.get_post_data(Bandeira=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_autorizacao_sem_cpf_funciona(self):
        post_data = self.get_post_data(CPFPortadorCartao=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_transacao_com_valor_float_funciona(self):
        post_data = self.get_post_data(ValorDocumento=1.1)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_quantidade_parcelas_pode_ser_omitida(self):
        post_data = self.get_post_data(QuantidadeParcelas=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_parcelamento_habilitado(self):
        post_data = self.get_post_data(
            ParcelamentoAdministradora='S', QuantidadeParcelas='10'
        )
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_extra_data_in_post_is_ignored(self):
        post_data = self.get_post_data(NaoFazDiferenca='sim', QuebraPost=False)
        wrapper = APC(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertTrue(result['approved'])
        self.assertEquals(result['failure_reason'], None)
        self.assertEquals(
            result['ResultadoSolicitacaoAprovacao'].split('-')[1].strip(),
            result['CodigoAutorizacao']
        )
        self.assertEquals(
            post_data['NumeroCartao'][:6],
            result['CartaoMascarado'][:6]
        )
        self.assertEquals(
            post_data['NumeroCartao'][-4:],
            result['CartaoMascarado'][-4:]
        )
        self.assertEquals(post_data['NumeroDocumento'], result['NumeroDocumento'])


class TestRecurringChargeValidation(BaseRecurringChargeTest):

    def test_quantidade_parcelas_negativa_gera_falha(self):
        post_data = self.get_post_data(QuantidadeParcelas=-3)
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('QuantidadeParcelas' in wrapper.errors)


    def test_autorizacao_sem_valor_falha(self):
        post_data = self.get_post_data(ValorDocumento=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('ValorDocumento' in wrapper.errors)


    def test_transacao_com_valor_de_tipo_invalido_falha(self):
        post_data = self.get_post_data(ValorDocumento='NoNumber')
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('ValorDocumento' in wrapper.errors)


    def test_transacao_sem_transacao_anterior_gera_falha(self):
        post_data = self.get_post_data(Transacao=None)
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('Transacao' in wrapper.errors)


    def test_endereco_ip_eh_RecorrENtE(self):
        post_data = self.get_post_data()
        wrapper = APC(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('EnderecoIPComprador' not in wrapper.errors)
        self.assertEquals(wrapper.request_data['EnderecoIPComprador'], 'RecorrENtE')
