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

    def plotar(self, x, y1, y2, y1_golay, y2_golay, tam, porcentagem_hamming, porcentagem_bch, porcentagem_ldpc, porcentagem_golay):
        # Plotando resultados LDPC/BCH/Hamming
        x_ldpcbchamming = self.fixPlot(x[0])
        y1_ldpcbchamming = self.fixPlot(y1)
        y2_ldpcbchamming = self.fixPlot(y2)
        self.plota_diferencas(x_ldpcbchamming, y1_ldpcbchamming, y2_ldpcbchamming, tam * 100)

        # Plotando resultados Golay
        x_golay = self.fixPlot(x[1])
        y1_golay = self.fixPlot(y1_golay)
        y2_golay = self.fixPlot(y2_golay)
        self.plota_diferencas(x_golay, y1_golay, y2_golay, len(x_golay))

        # Comparação de porcentagens de acertos
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(['Hamming', 'BCH', 'LDPC', 'Golay'], [porcentagem_hamming, porcentagem_bch, porcentagem_ldpc, porcentagem_golay],
               color=['blue', 'yellow', 'orange', 'red'])  # Mudança de cor do LDPC para laranja
        ax.set_xlabel('Método de Correção de Erros')
        ax.set_ylabel('Porcentagem de Acertos (%)')
        ax.set_title('Comparação de Porcentagem de Acertos entre Hamming, BCH, LDPC e Golay')
        plt.show()

    def plota_resultados_ldpc_bchamming(self, porcentagens_hamming, porcentagens_bch, porcentagens_ldpc, nBits):
        cenarios = ['Ruído Nulo Canal Unitário', 'Baixo Ruído Canal Unitário', 'Baixo Ruído Canal Rayleigh',
                    'Alto Ruído Canal Unitário', 'Alto Ruído Canal Rayleigh']

        barWidth = 0.25
        r1 = range(len(cenarios))
        r2 = [x + barWidth for x in r1]
        r3 = [y + barWidth for y in r2]

        plt.figure(figsize=(17, 7))
        bars_hamming = plt.bar(r1, porcentagens_hamming, color='b', width=barWidth, edgecolor='grey', label='Hamming')
        bars_bch = plt.bar(r2, porcentagens_bch, color='y', width=barWidth, edgecolor='grey', label='BCH')
        bars_ldpc = plt.bar(r3, porcentagens_ldpc, color='orange', width=barWidth, edgecolor='grey', label='LDPC')

        plt.xlabel('Cenários')
        plt.ylabel('Porcentagem de Acertos (%)')
        plt.title('Porcentagem de Acertos em Diferentes Cenários')
        plt.xticks([r + barWidth for r in range(len(cenarios))], cenarios)
        plt.legend()

        # Adicionando as porcentagens nas barras
        for bar in bars_hamming:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom')

        for bar in bars_bch:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom')

        for bar in bars_ldpc:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom')

        diretorio = r"C:\Users\Jaum\Desktop\Plots\1° RECONCILIAÇÃO\Maior distância"
        caminho_para_arquivo = os.path.join(diretorio, f'{nBits} bits para BCH_Hamming_LDPC.png')

        # Salva o plot no caminho especificado
        plt.savefig(caminho_para_arquivo)

        # Mostra o plot
        plt.show()

    def plota_resultados_golay(self, porcentagens_golay):
        cenarios = ['Ruído Nulo Canal Unitário', 'Baixo Ruído Canal Unitário', 'Baixo Ruído Canal Rayleigh',
                    'Alto Ruído Canal Unitário', 'Alto Ruído Canal Rayleigh']

        plt.figure(figsize=(15, 7))
        bars_golay = plt.bar(cenarios, porcentagens_golay, color='r', edgecolor='grey', label='Golay')

        plt.xlabel('Cenários')
        plt.ylabel('Porcentagem de Acertos (%)')
        plt.title('Porcentagem de Acertos em Diferentes Cenários')
        plt.legend()

        # Adicionando as porcentagens nas barras
        for bar in bars_golay:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom')

        diretorio = r"C:\Users\Jaum\Desktop\Plots\1° RECONCILIAÇÃO\Golay"
        caminho_para_arquivo = os.path.join(diretorio, f'24 bits para Golay.png')

        # Salva o plot no caminho especificado
        plt.savefig(caminho_para_arquivo)

        # Mostra o plot
        plt.show()
