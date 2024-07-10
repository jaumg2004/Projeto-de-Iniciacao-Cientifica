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

    def plotar(self, x, y1, y2, tam, porcentagem_hamming, porcentagem_bch):
        x = self.fixPlot(x)
        y1 = self.fixPlot(y1)
        y2 = self.fixPlot(y2)
        self.plota_diferencas(x, y1, y2, tam * 100)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(['Hamming', 'BCH'], [porcentagem_hamming, porcentagem_bch])
        ax.set_xlabel('Método de Correção de Erros')
        ax.set_ylabel('Porcentagem de Acertos (%)')
        ax.set_title('Comparação de Porcentagem de Acertos entre Hamming e BCH')

        plt.show()

    def plota_resultados(self, porcentagens_hamming, porcentagens_bch, nBits):
        cenarios = ['Ruído Nulo Canal Unitário', 'Baixo Ruído Canal Unitário', 'Baixo Ruído Canal Rayleigh',
                    'Alto Ruído Canal Unitário', 'Alto Ruído Canal Rayleigh']

        barWidth = 0.35
        r1 = range(len(cenarios))
        r2 = [x + barWidth for x in r1]

        plt.figure(figsize=(15, 7))
        plt.bar(r1, porcentagens_hamming, color='b', width=barWidth, edgecolor='grey', label='Hamming')
        plt.bar(r2, porcentagens_bch, color='g', width=barWidth, edgecolor='grey', label='BCH')

        plt.xlabel('Cenários')
        plt.ylabel('Porcentagem de Erros (%)')
        plt.title('Porcentagem de Erros em Diferentes Cenários')
        plt.xticks([r + barWidth/2 for r in r1], cenarios)
        plt.legend()

        diretorio = r"C:\Users\Jaum\Desktop\Plots"
        caminho_para_arquivo = os.path.join(diretorio, f'{nBits} bits.png')

        # Salva o plot no caminho especificado
        plt.savefig(caminho_para_arquivo)

        # Mostra o plot
        plt.show()
