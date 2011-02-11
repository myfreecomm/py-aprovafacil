# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from mock import Mock, patch
import time
from decimal import Decimal
from httplib2 import Http

from aprovafacil.wrapper import AprovaFacilWrapper
import mocked_responses

__all__ = ['TestAPC', 'TestAPCValidation']

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

class BaseAPCTest(TestCase)

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


class TestAPC(BaseAPCTest):

    @patch.object(Http, 'request', Mock(return_value=http_error))
    def test_erro_http(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data()
        result = wrapper.do_apc(**post_data)
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'],  'HTTP Error, status 500')


    @patch.object(Http, 'request', Mock(return_value=invalid_licence))
    def test_arquivo_licenca_invalido(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CodigoSeguranca=555)
        result = wrapper.do_apc(**post_data)
        self.assertFalse(result['approved'])
        self.assertEquals(
            result['failure_reason'],
            'CGI error. Check licence file'
        )


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_autorizacao_aprovada(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CodigoSeguranca=555)
        result = wrapper.do_apc(**post_data)
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
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CodigoSeguranca=501)
        result = wrapper.do_apc(**post_data)
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], AprovaFacilWrapper.FAILURE_REASONS['30'])
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
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CodigoSeguranca=502)
        result = wrapper.do_apc(**post_data)
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], AprovaFacilWrapper.FAILURE_REASONS['78'])


    @patch.object(Http, 'request', Mock(return_value=invalid_credit_card))
    def test_autorizacao_recusada_cartao_invalido(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CodigoSeguranca=504)
        result = wrapper.do_apc(**post_data)
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], AprovaFacilWrapper.FAILURE_REASONS['14'])


    @patch.object(Http, 'request', Mock(return_value=invalid_amount))
    def test_autorizacao_recusada_valor_invalido(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CodigoSeguranca=506)
        result = wrapper.do_apc(**post_data)
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], AprovaFacilWrapper.FAILURE_REASONS['60'])


    @patch.object(Http, 'request', Mock(return_value=duplicated_transaction))
    def test_autorizacao_recusada_transacao_ja_efetuada(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CodigoSeguranca=507)
        result = wrapper.do_apc(**post_data)
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], AprovaFacilWrapper.FAILURE_REASONS['68'])


    @patch.object(Http, 'request', Mock(return_value=expired_credit_card))
    def test_autorizacao_recusada_cartao_vencido(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CodigoSeguranca=508)
        result = wrapper.do_apc(**post_data)
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], AprovaFacilWrapper.FAILURE_REASONS['54'])


    @patch.object(Http, 'request', Mock(return_value=invalid_data))
    def test_autorizacao_recusada_dados_invalidos(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CodigoSeguranca=509)
        result = wrapper.do_apc(**post_data)
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], AprovaFacilWrapper.FAILURE_REASONS['56'])


    @patch.object(Http, 'request', Mock(return_value=invalid_security_code))
    def test_autorizacao_recusada_codigo_seguranca_invalido(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CodigoSeguranca=444)
        result = wrapper.do_apc(**post_data)
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], AprovaFacilWrapper.FAILURE_REASONS['N7'])


    @patch.object(Http, 'request', Mock(return_value=retry_transaction))
    def test_autorizacao_recusada_refaca_transacao(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CodigoSeguranca=333)
        result = wrapper.do_apc(**post_data)
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'], AprovaFacilWrapper.FAILURE_REASONS['84'])


    @patch.object(Http, 'request', Mock(return_value=accepted))
    def test_autorizacao_sem_nome_portador_funciona(self):
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(NomePortadorCartao=None)
        result = wrapper.do_apc(**post_data)
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
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(Bandeira=None)
        result = wrapper.do_apc(**post_data)
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
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(CPFPortadorCartao=None)
        result = wrapper.do_apc(**post_data)
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
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(ValorDocumento=1.1)
        result = wrapper.do_apc(**post_data)
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
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(QuantidadeParcelas=None)
        result = wrapper.do_apc(**post_data)
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
        wrapper = AprovaFacilWrapper(cgi_url=self.url)
        post_data = self.get_post_data(NaoFazDiferenca='sim', QuebraPost=False)
        result = wrapper.do_apc(**post_data)
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


class TestAPCValidation(BaseAPCTest):

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
