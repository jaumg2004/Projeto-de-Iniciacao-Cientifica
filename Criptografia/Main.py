import time
import numpy as np
import random

# Importa as classes necessárias
from CodeGenerator import CodeGenerator
from Cenário1 import RuidoNuloCanalUnitario
from Cenário2 import BaixoRuidoCanalUnitario
from Cenário3 import BaixoRuidoCanalRayleigh
from Cenário4 import AltoRuidoCanalUnitario
from Cenário5 import AltoRuidoCanalRayleigh
from Plotagem import Plotagem


def solicita_entrada(mensagem, tipo=int, validacao=None):
    """Solicita e valida a entrada do usuário."""
    while True:
        try:
            valor = tipo(input(mensagem))
            if validacao and not validacao(valor):
                raise ValueError("Entrada inválida.")
            return valor
        except ValueError as e:
            print(e)


def inicializa_variaveis(code, nBits):
    """Inicializa as variáveis globais para os cenários."""
    if code == 'Golay':
        x = [random.randint(0, 1) for _ in range(24)]
        h1 = np.random.rayleigh(1.0, 24)
        h2 = np.random.rayleigh(1.0, 24)
        golay = CodeGenerator(n_bits=24, code=code)
        tabela = golay.generate_code_table()
        size = None
    else:
        x = [random.randint(0, 1) for _ in range(nBits)]
        h1 = np.random.rayleigh(1.0, nBits)
        h2 = np.random.rayleigh(1.0, nBits)
        size = None if nBits <= 15 else solicita_entrada(
            "Entre com tamanho do espaço amostral: ", int, lambda v: v > 0
        )
        code_generator = CodeGenerator(nBits, code)
        tabela = code_generator.generate_code_table(size)

    return x, h1, h2, tabela, size


def inicializa_canais(media, variancia, ntestes, n_plot):
    """Inicializa os canais de comunicação."""
    return {
        "ruido_nulo": RuidoNuloCanalUnitario(media, variancia, ntestes, n_plot),
        "baixo_ruido_unitario": BaixoRuidoCanalUnitario(media, variancia, ntestes, n_plot),
        "baixo_ruido_rayleigh": BaixoRuidoCanalRayleigh(media, variancia, ntestes, n_plot),
        "alto_ruido_unitario": AltoRuidoCanalUnitario(media, variancia, ntestes, n_plot),
        "alto_ruido_rayleigh": AltoRuidoCanalRayleigh(media, variancia, ntestes, n_plot),
    }

def coletar_porcentagens(canais, x, h1, h2, plot, size, tabela, nBits, code):
    """Coleta as porcentagens de acertos para cada cenário."""
    return [
        canais["ruido_nulo"].cenario(x, plot, size, tabela, code),
        canais["baixo_ruido_unitario"].cenario(x, plot, size, tabela, code),
        canais["baixo_ruido_rayleigh"].cenario(x, h1, h2, plot, size, tabela, nBits, code),
        canais["alto_ruido_unitario"].cenario(x, plot, size, tabela, nBits, code),
        canais["alto_ruido_rayleigh"].cenario(x, h1, h2, plot, size, tabela, nBits, code),
    ]


# Marca o tempo inicial
start_time = time.time()

# Solicita parâmetros ao usuário
n_plot = solicita_entrada("Escolha o metodo de reconciliação, 1 ou 2? ", int, lambda v: v in {1, 2})
ntestes = solicita_entrada("Entre com a quantidade de testes: ", int, lambda v: v > 0)
code = solicita_entrada("Qual tabela vai ser utilizada: Hamming, BCH, LDPC ou Golay? \n", str, lambda v: v in {"Hamming", "BCH", "LDPC", "Golay"})
plot = 1 if solicita_entrada("Deseja realizar a Plotagem dos sinais? 'y' para sim, 'n' para nao \n", str, lambda v: v in {"y", "n"}) == "y" else 0

nBits = None if code == "Golay" else solicita_entrada("Entre com o tamanho da cadeia de Bits (7, 15, 127, 255): ", int, lambda v: v in {7, 15, 127, 255})

# Inicializa variáveis e canais
x, h1, h2, tabela, size = inicializa_variaveis(code, nBits)
canais = inicializa_canais(media=0.5, variancia=1.5, ntestes=ntestes, n_plot=n_plot)

# Coleta as porcentagens de acertos
porcentagens = coletar_porcentagens(canais, x, h1, h2, plot, size, tabela, nBits, code)

# Plota os resultados
Plotagem().plota(code, porcentagens, len(x), n_plot)

# Marca o tempo final e exibe o tempo de execução
execution_time = time.time() - start_time
hours, rem = divmod(execution_time, 3600)
minutes, seconds = divmod(rem, 60)
print(f"Tempo de execução da simulação: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
