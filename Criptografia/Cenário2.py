import random
from CenárioBase import CenárioBase
from Plotagem import Plotagem

class BaixoRuidoCanalUnitario(CenárioBase, Plotagem):
    def calculaY(self, x, variancia, media):
        # Generate noise with a normal distribution
        def geraRuido(variancia, media):
            return [random.gauss(media, variancia) for _ in range(len(x))]

        n = geraRuido(variancia, media)
        # Construct y based on noise addition and threshold
        y = [1 if x[i] + n[i] > 0.5 else 0 for i in range(len(x))]
        return y

    def cenario(self, x, plot, size, tabela, code):
        print("Cenário 2: Baixo Ruido Canal Unitario\n")

        contagem_de_acertos = 0

        for i in range(self.ntestes):
            print(f'Teste {i+1}/{self.ntestes}')
            print('x =', x)

            y1 = self.calculaY(x, self.variancia - 1.3, self.media)
            print('y1 =', y1)
            erros_y1 = self.encontraErros(x, y1)
            print('Erros do y1 =', erros_y1)

            y2 = self.calculaY(x, self.variancia - 1.3, self.media)
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

        # Calculate the percentage of success
        porcentagem_de_acertos = (contagem_de_acertos * 100.0) / self.ntestes
        print(f"Porcentagem de vezes que a chave gerada foi encontrada na tabela {code}: {porcentagem_de_acertos:.2f}%")

        if plot:
            self.plotar(x, y1, y2, len(x), porcentagem_de_acertos)

        return porcentagem_de_acertos
