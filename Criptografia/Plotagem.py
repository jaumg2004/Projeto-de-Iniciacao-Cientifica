from matplotlib import pyplot as plt

class Plotagem:
    def __init__(self):
        pass

    def plota_diferencas(self, x, y1, y2, tam):
        fig, axes = plt.subplots(nrows = 2, ncols = 1, figsize = (15, 7))

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

    def plotar(self, x, y1, y2, tam):
        x = self.fixPlot(x)
        y1 = self.fixPlot(y1)
        y2 = self.fixPlot(y2)
        self.plota_diferencas(x, y1, y2, tam * 100)

    def plota_resultados(self, porcentagens):
        cenarios = ['Ruído Nulo Canal Unitário', 'Baixo Ruído Canal Unitário', 'Baixo Ruído Canal Rayleigh',
                    'Alto Ruído Canal Unitário', 'Alto Ruído Canal Rayleigh']

        fig, ax = plt.subplots(figsize = (15, 7))
        ax.bar(cenarios, porcentagens)
        ax.set_xlabel('Cenários')
        ax.set_ylabel('Porcentagem de Erros (%)')
        ax.set_title('Porcentagem de Erros em Diferentes Cenários')

        plt.show()

