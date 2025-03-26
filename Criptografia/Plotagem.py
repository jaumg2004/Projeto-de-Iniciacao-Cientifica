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

        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 7), tight_layout=True)

        for ax, y_fixed, title in zip(axes, [y1_fixed, y2_fixed], ['Y1', 'Y2']):
            ax.plot(indices, x_fixed, 'r--', label='X')
            ax.plot(indices, y_fixed, 'b', label=title)
            ax.set_title(title)
            ax.set_xlabel('Índice do Bit')
            ax.set_ylabel('Valor do Bit')
            ax.legend()
            ax.margins(0)

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

        fig, ax = plt.subplots(figsize=(17, 7), tight_layout=True)
        bars = ax.bar(range(len(cenarios)), porcentagens, color=colors.get(code, 'grey'), edgecolor='grey', label=code)

        ax.set_xlabel('Cenários')
        ax.set_ylabel('Porcentagem de Acertos (%)')
        ax.set_title(f'Porcentagem de Acertos em Diferentes Cenários para {code}', pad=20)  # Adiciona espaço abaixo do título
        ax.set_xticks(range(len(cenarios)))
        ax.set_xticklabels(cenarios, rotation=0, ha='center')  # Mantém as legendas horizontais
        ax.legend()
        ax.margins(0)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}%', ha='center', va='bottom')

        diretorio = os.path.join(f"C:\\Users\\Jaum\\Desktop\\Plots\\{n_plot}° RECONCILIAÇÃO")
        os.makedirs(diretorio, exist_ok=True)
        caminho_para_arquivo = os.path.join(diretorio, f'{nBits} bits para {code}.png')

        plt.savefig(caminho_para_arquivo, bbox_inches='tight')
        plt.show()
