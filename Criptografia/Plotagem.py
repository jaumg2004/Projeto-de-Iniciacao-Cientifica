import os.path
from matplotlib import pyplot as plt

class Plotagem:
    def __init__(self):
        pass

    def plota_diferencas(self, x, y1, y2, tam):
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 7))

        indices = range(tam)  # Cria uma lista de índices de 0 a tam-1

        axes[0].plot(indices, x, 'r--', label='X')
        axes[0].plot(indices, y1, 'b', label='Y1')
        axes[0].set_title('Y1')
        axes[0].set_xlabel('Índice do Bit')
        axes[0].set_ylabel('Valor do Bit')
        axes[0].legend()

        axes[1].plot(indices, x, 'r--', label='X')
        axes[1].plot(indices, y2, 'b', label='Y2')
        axes[1].set_title('Y2')
        axes[1].set_xlabel('Índice do Bit')
        axes[1].set_ylabel('Valor do Bit')
        axes[1].legend()

        plt.tight_layout()
        plt.show()

    def fixPlot(self, aux):
        y = []
        for i in range(len(aux)):
            for k in range(100):
                y.append(aux[i])
        return y

    def plotar(self, x, y1, y2, tam, porcentagem_hamming, porcentagem_bch, porcentagem_golay):
        x = self.fixPlot(x)
        y1 = self.fixPlot(y1)
        y2 = self.fixPlot(y2)
        self.plota_diferencas(x, y1, y2, tam * 100)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(['Hamming', 'BCH', 'Golay'], [porcentagem_hamming, porcentagem_bch, porcentagem_golay])
        ax.set_xlabel('Método de Correção de Erros')
        ax.set_ylabel('Porcentagem de Acertos (%)')
        ax.set_title('Comparação de Porcentagem de Acertos entre Hamming, BCH e Golay')

        plt.show()

    def plota_resultados(self, porcentagens_hamming, porcentagens_bch, porcentagens_golay, nBits):
        cenarios = ['Ruído Nulo Canal Unitário', 'Baixo Ruído Canal Unitário', 'Baixo Ruído Canal Rayleigh',
                    'Alto Ruído Canal Unitário', 'Alto Ruído Canal Rayleigh']

        barWidth = 0.25
        r1 = range(len(cenarios))
        r2 = [x + barWidth for x in r1]
        r3 = [x + barWidth for x in r2]

        plt.figure(figsize=(15, 7))
        plt.bar(r1, porcentagens_hamming, color='b', width=barWidth, edgecolor='grey', label='Hamming')
        plt.bar(r2, porcentagens_bch, color='y', width=barWidth, edgecolor='grey', label='BCH')
        plt.bar(r3, porcentagens_golay, color='r', width=barWidth, edgecolor='grey', label='Golay')

        plt.xlabel('Cenários')
        plt.ylabel('Porcentagem de Acertos (%)')
        plt.title('Porcentagem de Acertos em Diferentes Cenários')
        plt.xticks([r + barWidth for r in range(len(cenarios))], cenarios)
        plt.legend()

        diretorio = r"C:\Users\Jaum\Desktop\Plots\10.0 scale"
        caminho_para_arquivo = os.path.join(diretorio, f'{nBits} bits.png')

        # Salva o plot no caminho especificado
        plt.savefig(caminho_para_arquivo)

        # Mostra o plot
        plt.show()
