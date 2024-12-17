import os.path
from matplotlib import pyplot as plt

class Plotagem:
    def __init__(self):
        pass

    def plota_diferencas(self, x, y1, y2, tam):
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 7))

        indices = range(tam * 100)  # Cria uma lista de índices de 0 a tam-1

        x = self.fixPlot(x)
        y1 = self.fixPlot(y1)
        y2 = self.fixPlot(y2)

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


    def plota_resultados_ldpc_bchamming(self, code, porcentagens, nBits):
        cenarios = ['Ruído Nulo Canal Unitário', 'Baixo Ruído Canal Unitário', 'Baixo Ruído Canal Rayleigh',
                    'Alto Ruído Canal Unitário', 'Alto Ruído Canal Rayleigh']

        r = range(len(cenarios))

        plt.figure(figsize=(17, 7))

        if code == 'Hamming':
            bars = plt.bar(r, porcentagens, color='b', edgecolor='grey', label='Hamming')

        if code == 'BCH':
            bars = plt.bar(r, porcentagens, color='y', edgecolor='grey', label='BCH')

        if code == 'LDPC':
            bars = plt.bar(r, porcentagens, color='orange', edgecolor='grey', label='LDPC')


        plt.xlabel('Cenários')
        plt.ylabel('Porcentagem de Acertos (%)')
        plt.title(f'Porcentagem de Acertos em Diferentes Cenários para {code}')
        plt.xticks([r for r in range(len(cenarios))], cenarios)
        plt.legend()

        # Adicionando as porcentagens nas barras
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom')

        diretorio = r"C:\Users\Jaum\Desktop\Plots\1° RECONCILIAÇÃO"
        caminho_para_arquivo = os.path.join(diretorio, f'{nBits} bits para {code}.png')

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
        plt.title('Porcentagem de Acertos em Diferentes Cenários para Golay')
        plt.legend()

        # Adicionando as porcentagens nas barras
        for bar in bars_golay:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom')

        diretorio = r"C:\Users\Jaum\Desktop\Plots\1° RECONCILIAÇÃO"
        caminho_para_arquivo = os.path.join(diretorio, f'24 bits para Golay.png')

        # Salva o plot no caminho especificado
        plt.savefig(caminho_para_arquivo)

        # Mostra o plot
        plt.show()
