# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from mock import Mock, patch
import time
from decimal import Decimal
from httplib2 import Http

from aprovafacil.wrapper import CAN, CAP
import mocked_responses

__all__ = [
    'TestCAP', 'TestCAPValidation',
    #'TestCAN', 'TestCANValidation',
]

http_200 = {'status': '200'}
http_500 = {'status': '500'}

http_error = (http_500, '')
invalid_licence = (http_200, mocked_responses.invalid_licence)
confirmed_capture = (http_200, mocked_responses.confirmed_capture)
failed_capture = (http_200, mocked_responses.failed_capture)

##
# CAN
##

class BaseCanCapTest(TestCase):

    def setUp(self):
      self.url = 'http://localhost/cgi-bin/CGIAprovaFacil'


    def get_post_data(self, **kwargs):
        post_data = {
            'NumeroDocumento': '1',
            'Transacao': '73417867510462'
        }
        post_data.update(**kwargs)
        return post_data


class TestCAN(BaseCanCapTest):

    @patch.object(Http, 'request', Mock(return_value=http_error))
    def test_erro_http(self):
        post_data = self.get_post_data()
        wrapper = CAN(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'],  'HTTP Error, status 500')


    @patch.object(Http, 'request', Mock(return_value=invalid_licence))
    def test_arquivo_licenca_invalido(self):
        post_data = self.get_post_data(CodigoSeguranca=555)
        wrapper = CAN(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(
            result['failure_reason'],
            'CGI error. Check licence file'
        )


    def test_cancelamento_com_sucesso(self):
        post_data = self.get_post_data()
        wrapper = CAN(cgi_url=self.url, **post_data)
        result = wrapper.make_request()


    def test_cancelamento_marcado_para_processamento(self):
        post_data = self.get_post_data()
        wrapper = CAN(cgi_url=self.url, **post_data)
        result = wrapper.make_request()


    def test_falha_no_cancelamento(self):
        post_data = self.get_post_data(CodigoSeguranca=501)
        wrapper = CAN(cgi_url=self.url, **post_data)
        result = wrapper.make_request()


    def test_erro_na_marcacao_para_cancelamento(self):
        post_data = self.get_post_data()
        wrapper = CAN(cgi_url=self.url, **post_data)
        result = wrapper.make_request()


class TestCANValidation(BaseCanCapTest):


    def test_numero_documento_eh_opcional(self):
        post_data = self.get_post_data(NumeroDocumento=None)
        wrapper = CAN(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertFalse('NumeroDocumento' in wrapper.errors)


    def test_transacao_anterior_eh_obrigatoria(self):
        post_data = self.get_post_data(Transacao=None)
        wrapper = CAN(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('Transacao' in wrapper.errors)

##
# CAP
##

class TestCAP(BaseCanCapTest):

    @patch.object(Http, 'request', Mock(return_value=http_error))
    def test_erro_http(self):
        post_data = self.get_post_data()
        wrapper = CAP(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(result['failure_reason'],  'HTTP Error, status 500')


    @patch.object(Http, 'request', Mock(return_value=invalid_licence))
    def test_arquivo_licenca_invalido(self):
        post_data = self.get_post_data(CodigoSeguranca=555)
        wrapper = CAP(cgi_url=self.url, **post_data)
        result = wrapper.make_request()
        self.assertFalse(result['approved'])
        self.assertEquals(
            result['failure_reason'],
            'CGI error. Check licence file'
        )


    @patch.object(Http, 'request', Mock(return_value=confirmed_capture))
    def test_captura_com_sucesso(self):
        post_data = self.get_post_data()
        wrapper = CAP(cgi_url=self.url, **post_data)
        result = wrapper.make_request()


    @patch.object(Http, 'request', Mock(return_value=failed_capture))
    def test_falha_na_captura(self):
        post_data = self.get_post_data()
        wrapper = CAP(cgi_url=self.url, **post_data)
        result = wrapper.make_request()


class TestCAPValidation(BaseCanCapTest):


    def test_numero_documento_eh_opcional(self):
        post_data = self.get_post_data(NumeroDocumento=None)
        wrapper = CAP(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertFalse('NumeroDocumento' in wrapper.errors)


    def test_transacao_anterior_eh_obrigatoria(self):
        post_data = self.get_post_data(Transacao=None)
        wrapper = CAP(cgi_url=self.url, **post_data)
        wrapper.validate()
        self.assertTrue('Transacao' in wrapper.errors)
