import random

from CenárioBase import CenárioBase
from Plotagem import Plotagem

class AltoRuidoCanalRayleigh(CenárioBase, Plotagem):
    def calculaY(self, h, x, variancia, media, ntestes):
        # Função para gerar ruído com distribuição normal
        def geraRuido(variancia, media):
            return [random.gauss(media, variancia + 1.3) for _ in range(len(x))]

        n = geraRuido(variancia, media)
        y = [1 if h[i] * x[i] + n[i] > 0.5 else 0 for i in range(len(x))]
        return y

    def cenario(self, x, h1, h2, plot, size, tabela, nBits, code):

        print("Cenário 5: Alto Ruido Canal Rayleigh\n")

        contagem_de_acertos = 0

        for i in range(self.ntestes):
            print(f'Teste {i+1}/{self.ntestes}')
            print('x =', x)

            y1 = self.calculaY(x, h1, self.variancia, self.media, nBits)
            print('y1 =', y1)
            erros_y1 = self.encontraErros(x, y1)
            print('Erros do y1 =', erros_y1)

            y2 = self.calculaY(x, h2, self.variancia, self.media, nBits)
            print('y2 =', y2)
            erros_y2 = self.encontraErros(x, y2)
            print('Erros do y2 =', erros_y2)

            if plot:
                self.plota_diferencas(x, y1, y2, len(x))

            toStringY1 = ''.join(map(str, y1))
            toStringY2 = ''.join(map(str, y2))

            if self.nplot == 1:
                chave = self.comparaSinais(toStringY2, self.encontraParidade(toStringY1, tabela), tabela)
                print(f"Chave gerada por código de {code}:", chave)

            elif self.nplot == 2:
                c = random.choice(tabela)
                s = self.xor_binary(toStringY1, c)
                c_B = self.xor_binary(toStringY2 , s)
                chave = self.xor_binary(s, self.comparacao_mais_proxima(c_B, tabela))
                print(f"Chave gerada por código de {code}:", chave)

            if toStringY1 == chave:
                contagem_de_acertos += 1
            else:
                print(f"Não são iguais por {code}")


            print("\n--------------------------------------------------------")


        porcentagem_de_acertos = contagem_de_acertos * 100.00 / self.ntestes
        print(f"Porcentagem de vezes que a chave gerada foi encontrada na tabela {code}: {porcentagem_de_acertos:.2f}%")

        if plot:
            self.plotar(x, y1, y2, len(x), porcentagem_de_acertos)

        return porcentagem_de_acertos