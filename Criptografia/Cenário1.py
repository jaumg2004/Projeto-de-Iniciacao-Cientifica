from CenárioBase import CenárioBase
from Plotagem import Plotagem

class RuidoNuloCanalUnitario(CenárioBase, Plotagem):
    def calculaY(self, x):
        return [1 if x[i] > 0.5 else 0 for i in range(len(x))]

    def cenario(self, x, plot, size, tabela, code):

        print("Cenário 1: Ruido Nulo Canal Unitario\n")

        contagem_de_acertos = 0

        for i in range(self.ntestes):
            print(f'Teste {i+1}/{self.ntestes}')
            print('x =', x)

            y1 = self.calculaY(x)
            print('y1 =', y1)
            erros_y1 = self.encontraErros(x, y1)
            print('Erros do y1 =', erros_y1)

            y2 = self.calculaY(x)
            print('y2 =', y2)
            erros_y2 = self.encontraErros(x, y2)
            print('Erros do y2 =', erros_y2)

            if plot:
                self.plota_diferencas(x, y1, y2, len(x))

            toStringY1 = ''.join(map(str, y1))
            toStringY2 = ''.join(map(str, y2))

            chave = self.comparaSinais(toStringY2, self.encontraParidade(toStringY1, tabela), tabela)
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
