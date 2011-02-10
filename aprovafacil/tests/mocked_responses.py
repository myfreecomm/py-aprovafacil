# -*- coding: utf-8 -*-

invalid_licence = """<html>
    <title>Cobre Bem Tecnologia - Aprova F&aacute;cil</title>
    <body>
    <table><tr><td colspan=2><center><font color="#FF0000"><b>Arquivo de Licenca Cartoes Creito Invalido !!!
    Erro na carga do Script Invalid Header</b></font></center></td></tr></table>
    </body>
    </html>"""

missing_parcels = """<ResultadoAPC>
    <TransacaoAprovada>
    False
    </TransacaoAprovada>
    <ResultadoSolicitacaoAprovacao>
    Erro - Numero Parcelas deve ser maior que zero
    </ResultadoSolicitacaoAprovacao>
    <CodigoAutorizacao>

    </CodigoAutorizacao>
    <Transacao>

    </Transacao>
    <CartaoMascarado>
    555566******8884
    </CartaoMascarado>
    <NumeroDocumento>
    1
    </NumeroDocumento>
    <ComprovanteAdministradora>

    </ComprovanteAdministradora>
    <NacionalidadeEmissor>

    </NacionalidadeEmissor>
    <ResultadoAVS>

    </ResultadoAVS>
    <EnderecoAVS>
    <Endereco>

    </Endereco>
    <Numero>

    </Numero>
    <Complemento>

    </Complemento>
    <Cep>

    </Cep>
    </EnderecoAVS>
    <CodigoAVS>

    </CodigoAVS>
    <MensagemAVS>

    </MensagemAVS>
    <MeusDados>
    </MeusDados>

    </ResultadoAPC>"""

refused = """<ResultadoAPC>
    <TransacaoAprovada>
    False
    </TransacaoAprovada>
    <ResultadoSolicitacaoAprovacao>
    N?o Autorizado - 30 - 30ALEATORIO
    </ResultadoSolicitacaoAprovacao>
    <CodigoAutorizacao>

    </CodigoAutorizacao>
    <Transacao>
    73417867302294
    </Transacao>
    <CartaoMascarado>
    555566******8884
    </CartaoMascarado>
    <NumeroDocumento>
    1
    </NumeroDocumento>
    <ComprovanteAdministradora>

    </ComprovanteAdministradora>
    <NacionalidadeEmissor>

    </NacionalidadeEmissor>
    <ResultadoAVS>

    </ResultadoAVS>
    <EnderecoAVS>
    <Endereco>

    </Endereco>
    <Numero>

    </Numero>
    <Complemento>

    </Complemento>
    <Cep>

    </Cep>
    </EnderecoAVS>
    <CodigoAVS>

    </CodigoAVS>
    <MensagemAVS>

    </MensagemAVS>
    <MeusDados>
    </MeusDados>

    </ResultadoAPC>"""

accepted = """<ResultadoAPC>
    <TransacaoAprovada>
    True
    </TransacaoAprovada>
    <ResultadoSolicitacaoAprovacao>
    Autoriza??o - 880608
    </ResultadoSolicitacaoAprovacao>
    <CodigoAutorizacao>
    880608
    </CodigoAutorizacao>
    <Transacao>
    73417867510462
    </Transacao>
    <CartaoMascarado>
    555566******8884
    </CartaoMascarado>
    <NumeroDocumento>
    1
    </NumeroDocumento>
    <ComprovanteAdministradora>
    040016APROVADA 000000 020519               ADMCART@                 XXXX     @0000000000000000                 00/00@@Estabelecimento@Rua do Estabelecimento 123@Rio de Janeiro - RJ@000000000000000@@PDV=00000000                NSU=000000@01/08/2010 00:00  AUTORIZ=000000 ONL-X@VENDA CREDITO A VISTA@@      VALOR VENDA:        1,90@@       RECONHECO E PAGAREI A@         IMPORTANCIA ACIMA@@@     --------------------------@                                      @@        CONFIRA A ASSINATURA@@        (CUPOM FISCAL: 000000)@        (NSU D-TEF   : 000000)@@990000
    </ComprovanteAdministradora>
    <NacionalidadeEmissor>

    </NacionalidadeEmissor>
    <ResultadoAVS>

    </ResultadoAVS>
    <EnderecoAVS>
    <Endereco>

    </Endereco>
    <Numero>

    </Numero>
    <Complemento>

    </Complemento>
    <Cep>

    </Cep>
    </EnderecoAVS>
    <CodigoAVS>

    </CodigoAVS>
    <MensagemAVS>

    </MensagemAVS>
    <MeusDados>
    </MeusDados>

    </ResultadoAPC>"""

revoked_credit_card = """<ResultadoAPC>
    <TransacaoAprovada>
    False
    </TransacaoAprovada>
    <ResultadoSolicitacaoAprovacao>
    N?o Autorizado - 78 - 78CAR BLOQ1.USO
    </ResultadoSolicitacaoAprovacao>
    <CodigoAutorizacao>

    </CodigoAutorizacao>
    <Transacao>
    73417872982348
    </Transacao>
    <CartaoMascarado>
    555566******8884
    </CartaoMascarado>
    <NumeroDocumento>
    1
    </NumeroDocumento>
    <ComprovanteAdministradora>

    </ComprovanteAdministradora>
    <NacionalidadeEmissor>

    </NacionalidadeEmissor>
    <ResultadoAVS>

    </ResultadoAVS>
    <EnderecoAVS>
    <Endereco>

    </Endereco>
    <Numero>

    </Numero>
    <Complemento>

    </Complemento>
    <Cep>

    </Cep>
    </EnderecoAVS>
    <CodigoAVS>

    </CodigoAVS>
    <MensagemAVS>

    </MensagemAVS>
    <MeusDados>
    </MeusDados>

    </ResultadoAPC>"""

invalid_credit_card = """<ResultadoAPC>
    <TransacaoAprovada>
    False
    </TransacaoAprovada>
    <ResultadoSolicitacaoAprovacao>
    N?o Autorizado - 14 - 14CARTAOINVALIDO
    </ResultadoSolicitacaoAprovacao>
    <CodigoAutorizacao>

    </CodigoAutorizacao>
    <Transacao>
    73417872986389
    </Transacao>
    <CartaoMascarado>
    555566******8884
    </CartaoMascarado>
    <NumeroDocumento>
    1
    </NumeroDocumento>
    <ComprovanteAdministradora>

    </ComprovanteAdministradora>
    <NacionalidadeEmissor>

    </NacionalidadeEmissor>
    <ResultadoAVS>

    </ResultadoAVS>
    <EnderecoAVS>
    <Endereco>

    </Endereco>
    <Numero>

    </Numero>
    <Complemento>

    </Complemento>
    <Cep>

    </Cep>
    </EnderecoAVS>
    <CodigoAVS>

    </CodigoAVS>
    <MensagemAVS>

    </MensagemAVS>
    <MeusDados>
    </MeusDados>

    </ResultadoAPC>"""

expired_credit_card="""<ResultadoAPC>
    <TransacaoAprovada>
    False
    </TransacaoAprovada>
    <ResultadoSolicitacaoAprovacao>
    N?o Autorizado - 54 - 54CARTAO VENCIDO
    </ResultadoSolicitacaoAprovacao>
    <CodigoAutorizacao>

    </CodigoAutorizacao>
    <Transacao>
    73417872990431
    </Transacao>
    <CartaoMascarado>
    555566******8884
    </CartaoMascarado>
    <NumeroDocumento>
    1
    </NumeroDocumento>
    <ComprovanteAdministradora>

    </ComprovanteAdministradora>
    <NacionalidadeEmissor>

    </NacionalidadeEmissor>
    <ResultadoAVS>

    </ResultadoAVS>
    <EnderecoAVS>
    <Endereco>

    </Endereco>
    <Numero>

    </Numero>
    <Complemento>

    </Complemento>
    <Cep>

    </Cep>
    </EnderecoAVS>
    <CodigoAVS>

    </CodigoAVS>
    <MensagemAVS>

    </MensagemAVS>
    <MeusDados>
    </MeusDados>

    </ResultadoAPC>"""

invalid_security_code = """<ResultadoAPC>
    <TransacaoAprovada>
    False
    </TransacaoAprovada>
    <ResultadoSolicitacaoAprovacao>
    N?o Autorizado - N7 - N7COD.SEG.INVAL
    </ResultadoSolicitacaoAprovacao>
    <CodigoAutorizacao>

    </CodigoAutorizacao>
    <Transacao>
    73417872992472
    </Transacao>
    <CartaoMascarado>
    555566******8884
    </CartaoMascarado>
    <NumeroDocumento>
    1
    </NumeroDocumento>
    <ComprovanteAdministradora>

    </ComprovanteAdministradora>
    <NacionalidadeEmissor>

    </NacionalidadeEmissor>
    <ResultadoAVS>

    </ResultadoAVS>
    <EnderecoAVS>
    <Endereco>

    </Endereco>
    <Numero>

    </Numero>
    <Complemento>

    </Complemento>
    <Cep>

    </Cep>
    </EnderecoAVS>
    <CodigoAVS>

    </CodigoAVS>
    <MensagemAVS>

    </MensagemAVS>
    <MeusDados>
    </MeusDados>

    </ResultadoAPC>"""

retry_transaction = """<ResultadoAPC>
    <TransacaoAprovada>
    False
    </TransacaoAprovada>
    <ResultadoSolicitacaoAprovacao>
    N?o Autorizado - 84 - T84REFACA TRANS
    </ResultadoSolicitacaoAprovacao>
    <CodigoAutorizacao>

    </CodigoAutorizacao>
    <Transacao>
    73417872997558
    </Transacao>
    <CartaoMascarado>
    555566******8884
    </CartaoMascarado>
    <NumeroDocumento>
    1
    </NumeroDocumento>
    <ComprovanteAdministradora>

    </ComprovanteAdministradora>
    <NacionalidadeEmissor>

    </NacionalidadeEmissor>
    <ResultadoAVS>

    </ResultadoAVS>
    <EnderecoAVS>
    <Endereco>

    </Endereco>
    <Numero>

    </Numero>
    <Complemento>

    </Complemento>
    <Cep>

    </Cep>
    </EnderecoAVS>
    <CodigoAVS>

    </CodigoAVS>
    <MensagemAVS>

    </MensagemAVS>
    <MeusDados>
    </MeusDados>

    </ResultadoAPC>"""

duplicated_transaction = """<ResultadoAPC>
    <TransacaoAprovada>
    False
    </TransacaoAprovada>
    <ResultadoSolicitacaoAprovacao>
    N?o Autorizado - 68 - T68TRANSACAO JA EFETUADA
    </ResultadoSolicitacaoAprovacao>
    <CodigoAutorizacao>

    </CodigoAutorizacao>
    <Transacao>
    73417873001598
    </Transacao>
    <CartaoMascarado>
    555566******8884
    </CartaoMascarado>
    <NumeroDocumento>
    1
    </NumeroDocumento>
    <ComprovanteAdministradora>

    </ComprovanteAdministradora>
    <NacionalidadeEmissor>

    </NacionalidadeEmissor>
    <ResultadoAVS>

    </ResultadoAVS>
    <EnderecoAVS>
    <Endereco>

    </Endereco>
    <Numero>

    </Numero>
    <Complemento>

    </Complemento>
    <Cep>

    </Cep>
    </EnderecoAVS>
    <CodigoAVS>

    </CodigoAVS>
    <MensagemAVS>

    </MensagemAVS>
    <MeusDados>
    </MeusDados>

    </ResultadoAPC>"""

missing_amount = """<ResultadoAPC>
    <TransacaoAprovada>
    False
    </TransacaoAprovada>
    <ResultadoSolicitacaoAprovacao>
    Erro - Valor deve ser maior que zero
    </ResultadoSolicitacaoAprovacao>
    <CodigoAutorizacao>

    </CodigoAutorizacao>
    <Transacao>

    </Transacao>
    <CartaoMascarado>
    Cartao Nao Informado
    </CartaoMascarado>
    <NumeroDocumento>

    </NumeroDocumento>
    <ComprovanteAdministradora>

    </ComprovanteAdministradora>
    <NacionalidadeEmissor>

    </NacionalidadeEmissor>
    <ResultadoAVS>

    </ResultadoAVS>
    <EnderecoAVS>
    <Endereco>

    </Endereco>
    <Numero>

    </Numero>
    <Complemento>

    </Complemento>
    <Cep>

    </Cep>
    </EnderecoAVS>
    <CodigoAVS>

    </CodigoAVS>
    <MensagemAVS>

    </MensagemAVS>
    <MeusDados>
    </MeusDados>

    </ResultadoAPC>"""

invalid_amount = """<ResultadoAPC>
    <TransacaoAprovada>
    False
    </TransacaoAprovada>
    <ResultadoSolicitacaoAprovacao>
    N?o Autorizado - 60 - Valor Inv?lido. Por favor, ent
    </ResultadoSolicitacaoAprovacao>
    <CodigoAutorizacao>

    </CodigoAutorizacao>
    <Transacao>
    73417873003644
    </Transacao>
    <CartaoMascarado>
    555566******8884
    </CartaoMascarado>
    <NumeroDocumento>
    1
    </NumeroDocumento>
    <ComprovanteAdministradora>

    </ComprovanteAdministradora>
    <NacionalidadeEmissor>

    </NacionalidadeEmissor>
    <ResultadoAVS>

    </ResultadoAVS>
    <EnderecoAVS>
    <Endereco>

    </Endereco>
    <Numero>

    </Numero>
    <Complemento>

    </Complemento>
    <Cep>

    </Cep>
    </EnderecoAVS>
    <CodigoAVS>

    </CodigoAVS>
    <MensagemAVS>

    </MensagemAVS>
    <MeusDados>
    </MeusDados>

    </ResultadoAPC>"""

invalid_data = """<ResultadoAPC>
    <TransacaoAprovada>
    False
    </TransacaoAprovada>
    <ResultadoSolicitacaoAprovacao>
    N?o Autorizado - 56 - Dado Inv?lido. Por favor, entr
    </ResultadoSolicitacaoAprovacao>
    <CodigoAutorizacao>

    </CodigoAutorizacao>
    <Transacao>
    73417875721753
    </Transacao>
    <CartaoMascarado>
    555566******8884
    </CartaoMascarado>
    <NumeroDocumento>
    1
    </NumeroDocumento>
    <ComprovanteAdministradora>

    </ComprovanteAdministradora>
    <NacionalidadeEmissor>

    </NacionalidadeEmissor>
    <ResultadoAVS>

    </ResultadoAVS>
    <EnderecoAVS>
    <Endereco>

    </Endereco>
    <Numero>

    </Numero>
    <Complemento>

    </Complemento>
    <Cep>

    </Cep>
    </EnderecoAVS>
    <CodigoAVS>

    </CodigoAVS>
    <MensagemAVS>

    </MensagemAVS>
    <MeusDados>
    </MeusDados>

    </ResultadoAPC>"""
