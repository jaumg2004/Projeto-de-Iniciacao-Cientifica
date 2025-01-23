import os
from matplotlib import pyplot as plt

class Plotagem:
    def __init__(self):
        pass

    @staticmethod
    def fix_plot(data):
        return [value for value in data for _ in range(100)]

    def plota_diferencas(self, x, y1, y2, tam):
        indices = range(tam * 100)

        x_fixed = self.fix_plot(x)
        y1_fixed = self.fix_plot(y1)
        y2_fixed = self.fix_plot(y2)

        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 7))

        axes[0].plot(indices, x_fixed, 'r--', label='X')
        axes[0].plot(indices, y1_fixed, 'b', label='Y1')
        axes[0].set_title('Y1')
        axes[0].set_xlabel('Índice do Bit')
        axes[0].set_ylabel('Valor do Bit')
        axes[0].legend()

        axes[1].plot(indices, x_fixed, 'r--', label='X')
        axes[1].plot(indices, y2_fixed, 'b', label='Y2')
        axes[1].set_title('Y2')
        axes[1].set_xlabel('Índice do Bit')
        axes[1].set_ylabel('Valor do Bit')
        axes[1].legend()

        plt.tight_layout()
        plt.show()

    def plota_resultados_ldpc_bchamming(self, code, porcentagens, nBits, n_plot):
        cenarios = [
            'Ruído Nulo Canal Unitário',
            'Baixo Ruído Canal Unitário',
            'Baixo Ruído Canal Rayleigh',
            'Alto Ruído Canal Unitário',
            'Alto Ruído Canal Rayleigh'
        ]

        colors = {'Hamming': 'b', 'BCH': 'y', 'LDPC': 'orange'}

        plt.figure(figsize=(17, 7))

        bars = plt.bar(range(len(cenarios)), porcentagens, color=colors.get(code, 'grey'), edgecolor='grey', label=code)

        plt.xlabel('Cenários')
        plt.ylabel('Porcentagem de Acertos (%)')
        plt.title(f'Porcentagem de Acertos em Diferentes Cenários para {code}')
        plt.xticks(range(len(cenarios)), cenarios)
        plt.legend()

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom')

        diretorio = os.path.join(f"C:\\Users\\Jaum\\Desktop\\Plots\\{n_plot}° RECONCILIAÇÃO")
        os.makedirs(diretorio, exist_ok=True)
        caminho_para_arquivo = os.path.join(diretorio, f'{nBits} bits para {code}.png')

        plt.savefig(caminho_para_arquivo)
        plt.show()

    def plota_resultados_golay(self, porcentagens_golay, n_plot):
        cenarios = [
            'Ruído Nulo Canal Unitário',
            'Baixo Ruído Canal Unitário',
            'Baixo Ruído Canal Rayleigh',
            'Alto Ruído Canal Unitário',
            'Alto Ruído Canal Rayleigh'
        ]

        plt.figure(figsize=(15, 7))
        bars = plt.bar(cenarios, porcentagens_golay, color='r', edgecolor='grey', label='Golay')

        plt.xlabel('Cenários')
        plt.ylabel('Porcentagem de Acertos (%)')
        plt.title('Porcentagem de Acertos em Diferentes Cenários para Golay')
        plt.legend()

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom')

        diretorio = os.path.join(f"C:\\Users\\Jaum\\Desktop\\Plots\\{n_plot}° RECONCILIAÇÃO")
        os.makedirs(diretorio, exist_ok=True)
        caminho_para_arquivo = os.path.join(diretorio, '24 bits para Golay.png')

        plt.savefig(caminho_para_arquivo)
        plt.show()
