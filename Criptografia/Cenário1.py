from CenárioBase import CenárioBase
from Plotagem import Plotagem
from Hamming import Hamming
from BCH import BCH
from Golay import Golay
from LDPC import LDPC

class RuidoNuloCanalUnitario(CenárioBase, Plotagem):
    def calculaY(self, x, testes):
        return [1 if x[i] > 0.5 else 0 for i in range(testes)]

    def cenario(self, x, nBits, plot, size):

        print("Cenário 1: Ruido Nulo Canal Unitario\n")

        n1 = nBits

        hamming = Hamming()

        bch = BCH(n1)
        tabelaBCH = bch.generate_code_table(size)

        ldpc = LDPC(n1)
        tabelaLDPC = ldpc.generate_code_table(size)

        golay = Golay()
        tabelaGolay = golay.generate_code_table()

        if n1 == 7:
            tabelaHamming = ['0000000', '1101001', '0101010', '1000011', '1001100', '0100101', '1100110', '0001111',
                             '1110000', '0011001', '1011010', '0110011', '0111100', '1010101', '0010110', '1111111']
        elif n1 == 15:
            tabelaHamming = hamming.generate_hamming_codes_15_bits()
        elif n1 == 31:
            tabelaHamming = hamming.generate_space_amostral_sample_31_bits(size)
        elif n1 == 63:
            tabelaHamming = hamming.generate_space_amostral_sample_63_bits(size)
        elif n1 == 127:
            tabelaHamming = hamming.generate_space_amostral_sample_127_bits(size)
        elif n1 == 255:
            tabelaHamming = hamming.generate_space_amostral_sample_255_bits(size)
        else:
            raise ValueError("Número de bits não suportado")

        print(tabelaHamming)

        contagem_de_acertos_Hamming = 0
        contagem_de_acertos_BCH = 0
        contagem_de_acertos_LDPC = 0
        contagem_de_acertos_Golay = 0

        for i in range(self.ntestes):
            print(f'Teste {i+1}/{self.ntestes}')
            print('x =', x)

            y1 = self.calculaY(x[0], n1)
            print('y1 =', y1)
            erros_y1 = self.encontraErros(x[0], y1)
            print('Erros do y1 =', erros_y1)

            y2 = self.calculaY(x[0], n1)
            print('y2 =', y2)
            erros_y2 = self.encontraErros(x[0], y2)
            print('Erros do y2 =', erros_y2)

            toStringY1 = ''.join(map(str, y1))
            toStringY2 = ''.join(map(str, y2))

            y1_golay = self.calculaY(x[1], 24)
            print('y1 de Golay =', y1_golay)
            y2_golay = self.calculaY(x[1], 24)
            print('y2 de Golay =', y2_golay)

            toStringY1_golay = ''.join(map(str, y1_golay))
            toStringY2_golay = ''.join(map(str, y2_golay))

            chave1 = self.comparaSinais(toStringY2, self.encontraParidade(toStringY1, tabelaHamming), tabelaHamming)
            print("Chave gerada por código de Hamming:", chave1)

            chave2 = self.comparaSinais(toStringY2, self.encontraParidade(toStringY1, tabelaBCH), tabelaBCH)
            print("Chave gerada por código BCH:", chave2)

            chave3 = self.comparaSinais(toStringY2, self.encontraParidade(toStringY1, tabelaLDPC), tabelaLDPC)
            print("Chave gerada por código LDPC:", chave3)

            chave4 = self.comparaSinais(toStringY2_golay, self.encontraParidade(toStringY1_golay, tabelaGolay), tabelaGolay)
            print("Chave gerada por código Golay:", chave4)

            if toStringY1 == chave1:
                contagem_de_acertos_Hamming += 1
            else:
                print("Não são iguais por Hamming")

            if toStringY1 == chave2:
                contagem_de_acertos_BCH += 1
            else:
                print("Não são iguais por BCH")

            if toStringY1 == chave3:
                contagem_de_acertos_LDPC += 1
            else:
                print("Não são iguais por LDPC")

            if toStringY1_golay == chave4:
                contagem_de_acertos_Golay += 1
            else:
                print("Não são iguais por Golay")

            print("\n--------------------------------------------------------")


        porcentagem_de_acertos_Hamming = contagem_de_acertos_Hamming * 100.00 / self.ntestes
        print(f"Porcentagem de vezes que a chave gerada foi encontrada na tabela Hamming: {porcentagem_de_acertos_Hamming:.2f}%")

        porcentagem_de_acertos_BCH = contagem_de_acertos_BCH * 100.00 / self.ntestes
        print(f"Porcentagem de vezes que a chave gerada foi descoberta por BCH: {porcentagem_de_acertos_BCH:.2f}%")

        porcentagem_de_acertos_LDPC = contagem_de_acertos_LDPC * 100.00 / self.ntestes
        print(f"Porcentagem de vezes que a chave gerada foi descoberta por LDPC: {porcentagem_de_acertos_LDPC:.2f}%")

        porcentagem_de_acertos_Golay = contagem_de_acertos_Golay * 100.00 / self.ntestes
        print(f"Porcentagem de vezes que a chave gerada foi encontrada na tabela Golay: {porcentagem_de_acertos_Golay:.2f}%\n")

        if plot:
            self.plotar(x, y1, y2, y1_golay, y2_golay, len(x[0]), porcentagem_de_acertos_Hamming, porcentagem_de_acertos_BCH, porcentagem_de_acertos_LDPC, porcentagem_de_acertos_Golay)

        return porcentagem_de_acertos_Hamming, porcentagem_de_acertos_BCH, porcentagem_de_acertos_LDPC, porcentagem_de_acertos_Golay
