import random

from CenárioBase import CenárioBase
from Plotagem import Plotagem
from Hamming import HammingCodeGenerator

class AltoRuidoCanalUnitario(CenárioBase, Plotagem, HammingCodeGenerator):
    def calculaY(self, x, variancia, media, ntestes):
        # Função para gerar ruído com distribuição normal
        def geraRuido(variancia, media, ntestes):
            return [random.gauss(media, variancia + 1.3) for _ in range(ntestes)]

        n = geraRuido(variancia, media, ntestes)
        y = [x[i] + n[i] for i in range(ntestes)]
        return [1 if y[i] > 0.5 else 0 for i in range(ntestes)]

    def cenario(self, x, nBits, plot):

        print("Cenário 4: Alto Ruido Canal Unitario\n")

        n4 = nBits

        if n4 == 7:
            tabela_Hamming = ['0000000', '1101001', '0101010', '1000011', '1001100', '0100101', '1100110', '0001111',
                      '1110000', '0011001', '1011010', '0110011', '0111100', '1010101', '0010110', '1111111']
        elif n4 == 15:
            tabela_Hamming = self.generate_hamming_codes_15_bits()
        elif n4 == 31:
            tabela_Hamming = self.generate_space_amostral_sample_31_bits(self.ntestes)
        elif n4 == 63:
            tabela_Hamming = self.generate_space_amostral_sample_63_bits(self.ntestes)
        elif n4 == 127:
            tabela_Hamming = self.generate_space_amostral_sample_127_bits(self.ntestes)
        elif n4 == 255:
            tabela_Hamming = self.generate_space_amostral_sample_255_bits(self.ntestes)
        else:
            raise ValueError("Número de bits não suportado")

        contagem_de_acertos_Hamming = 0
        contagem_de_acertos_BCH = 0

        for i in range(self.ntestes):
            print(f'Teste {i+1}/{self.ntestes}')
            print('x =', x)

            y1 = self.calculaY(x, self.variancia, self.media, n4)
            print('y1 =', y1)
            erros_y1 = self.encontraErros(x, y1)
            print('Erros do y1 =', erros_y1)

            y2 = self.calculaY(x, self.variancia, self.media, n4)
            print('y2 =', y2)
            erros_y2 = self.encontraErros(x, y2)
            print('Erros do y2 =', erros_y2)

            toStringY1 = ''.join(map(str, y1))
            toStringY2 = ''.join(map(str, y2))
            P = self.encontraParidade(y1, tabela_Hamming)
            chave1 = self.comparaSinais(y2, P, tabela_Hamming)
            print("Chave gerada por código de Hamming:", chave1)

            chave2 = self.test_bch_key_agreement(toStringY1, toStringY2, tabela_Hamming)
            print("Chave gerada por código BCH:", chave2)

            if toStringY1 == chave1:
                contagem_de_acertos_Hamming += 1
            else:
                print("Não são iguais por Hamming")

            if toStringY1 == chave2:
                contagem_de_acertos_BCH += 1
            else:
                print("Não são iguais por BCH")

            print("\n--------------------------------------------------------")

            if plot:
                self.plotar(x, y1, y2, len(x))


        porcentagem_de_acertos_Hamming = contagem_de_acertos_Hamming * 100.00 / self.ntestes
        print(f"Porcentagem de vezes que a chave gerada foi encontrada na tabela Hamming: {porcentagem_de_acertos_Hamming:.2f}%")

        porcentagem_de_acertos_BCH = contagem_de_acertos_BCH * 100.00 / self.ntestes
        print(f"Porcentagem de vezes que a chave gerada foi descoberta por BCH: {porcentagem_de_acertos_BCH:.2f}%\n")

        return porcentagem_de_acertos_Hamming, porcentagem_de_acertos_BCH