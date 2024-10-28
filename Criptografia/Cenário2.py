import random

from CenárioBase import CenárioBase
from Plotagem import Plotagem

class BaixoRuidoCanalUnitario(CenárioBase, Plotagem):
    def calculaY(self, x, variancia, media, ntestes):
        # Função para gerar ruído com distribuição normal
        def geraRuido(variancia, media, ntestes):
            return [random.gauss(media, variancia) for _ in range(ntestes)]

        n = geraRuido(variancia, media, ntestes)
        y = [x[i] + n[i] for i in range(ntestes)]
        return [1 if y[i] > 0.5 else 0 for i in range(ntestes)]

    def cenario(self, x, nBits, plot, size, tabela):

        print("Cenário 2: Baixo Ruido Canal Unitario\n")

        contagem_de_acertos_Hamming = 0
        contagem_de_acertos_BCH = 0
        contagem_de_acertos_LDPC = 0
        contagem_de_acertos_Golay = 0


        for i in range(self.ntestes):
            print(f'Teste {i+1}/{self.ntestes}')
            print('x =', x)

            y1 = self.calculaY(x[0], self.variancia - 1.3, self.media, nBits)
            print('y1 =', y1)
            erros_y1 = self.encontraErros(x[0], y1)
            print('Erros do y1 =', erros_y1)

            y2 = self.calculaY(x[0], self.variancia - 1.3, self.media, nBits)
            print('y2 =', y2)
            erros_y2 = self.encontraErros(x[0], y2)
            print('Erros do y2 =', erros_y2)

            toStringY1 = ''.join(map(str, y1))
            toStringY2 = ''.join(map(str, y2))

            y1_golay = self.calculaY(x[1], self.variancia - 1.3, self.media, 24)
            print('y1 de Golay =', y1_golay)
            y2_golay = self.calculaY(x[1], self.variancia - 1.3, self.media, 24)
            print('y2 de Golay =', y2_golay)

            toStringY1_golay = ''.join(map(str, y1_golay))
            toStringY2_golay = ''.join(map(str, y2_golay))

            # Comparação das chaves geradas
            chave1 = self.comparaSinais(toStringY2, self.encontraParidade(toStringY1, tabela[0]), tabela[0])
            print("Chave gerada por código de Hamming:", chave1)
            chave2 = self.comparaSinais(toStringY2, self.encontraParidade(toStringY1, tabela[1]), tabela[1])
            print("Chave gerada por código BCH:", chave2)
            chave3 = self.comparaSinais(toStringY2, self.encontraParidade(toStringY1, tabela[2]), tabela[2])
            print("Chave gerada por código LDPC:", chave3)
            chave4 = self.comparaSinais(toStringY2_golay, self.encontraParidade(toStringY1_golay, tabela[3]), tabela[3])
            print("Chave gerada por código Golay:", chave4)

            # Contagem de acertos
            if toStringY1 == chave1:
                contagem_de_acertos_Hamming += 1
            if toStringY1 == chave2:
                contagem_de_acertos_BCH += 1
            if toStringY1 == chave3:
                contagem_de_acertos_LDPC += 1
            if toStringY1_golay == chave4:
                contagem_de_acertos_Golay += 1

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