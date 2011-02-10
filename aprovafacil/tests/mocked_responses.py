# -*- coding: utf-8 -*-

invalid_licence = """<html>
    <title>Cobre Bem Tecnologia - Aprova F&aacute;cil</title>
    <body>
    <table><tr><td colspan=2><center><font color="#FF0000"><b>Arquivo de Licenca Cartoes Creito Invalido !!!
    Erro na carga do Script Invalid Header</b></font></center></td></tr></table>
    </body>
    </html>"""

amount_missing = """<ResultadoAPC>
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

parcels_missing = """<ResultadoAPC>
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
