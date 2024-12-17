import time
import numpy as np
import random

# Classes das tabelas
from CodeGenerator import CodeGenerator

# Classes dos canais
from Cenário1 import RuidoNuloCanalUnitario
from Cenário2 import BaixoRuidoCanalUnitario
from Cenário3 import BaixoRuidoCanalRayleigh
from Cenário4 import AltoRuidoCanalUnitario
from Cenário5 import AltoRuidoCanalRayleigh

# Classe de plotagem
from Plotagem import Plotagem

# Marca o tempo inicial
start_time = time.time()

# Variáveis globais
media = 0.5
variancia = 1.5

# Solicita ao usuário a quantidade de testes
ntestes = int(input("Entre com a quantidade de testes: "))

# Solicita qual o código corretor a ser usado
code = input("Qual tabela vai ser utilizada: Hamming, BCH, LDPC ou Golay? \n")

# Solicita se deseja realizar a plotagem
comando = input("Deseja realizar a Plotagem dos sinais? 'y' para sim, 'n' para nao \n")
plot = 1 if comando == 'y' else 0

# Inicializa variáveis
nBits = None
tabela = None
x = []
h1 = []
h2 = []

if code == 'Golay':
    x = [random.randint(0, 1) for _ in range(24)]
    h1 = np.random.rayleigh(1.0, 24)
    h2 = np.random.rayleigh(1.0, 24)
    golay = CodeGenerator(n_bits=24, code=code)
    tabela = golay.generate_code_table()
    size = None
else:
    while nBits not in {7, 15, 127, 255}:
        nBits = int(input("Entre com um dos valores possíveis para o tamanho da cadeia de Bits (7, 15, 127, 255): "))

    size = None
    if nBits > 15:
        size = int(input("Entre com tamanho do espaço amostral: "))

    # Gera uma lista de bits aleatórios (0 ou 1)
    x = [random.randint(0, 1) for _ in range(nBits)]

    # Amostras de canais de Rayleigh
    h1 = np.random.rayleigh(1.0, nBits)
    h2 = np.random.rayleigh(1.0, nBits)

    code_generator = CodeGenerator(nBits, code)
    tabela = code_generator.generate_code_table(size)

# Inicializa canais de comunicação
ruidoNuloCanalUnitario = RuidoNuloCanalUnitario(media, variancia, ntestes)
baixoRuidoCanalUnitario = BaixoRuidoCanalUnitario(media, variancia, ntestes)
baixoRuidoCanalRayleigh = BaixoRuidoCanalRayleigh(media, variancia, ntestes)
altoRuidoCanalUnitario = AltoRuidoCanalUnitario(media, variancia, ntestes)
altoRuidoCanalRayleigh = AltoRuidoCanalRayleigh(media, variancia, ntestes)

def coletar_porcentagens():
    porcentagens = []
    # Cenário de Ruído Nulo Canal Unitário
    porcentagens.append(ruidoNuloCanalUnitario.cenario(x, plot, size, tabela, code))
    # Cenário de Baixo Ruído Canal Unitário
    porcentagens.append(baixoRuidoCanalUnitario.cenario(x, plot, size, tabela, code))
    # Cenário de Baixo Ruído Canal Rayleigh
    porcentagens.append(baixoRuidoCanalRayleigh.cenario(x, h1, h2, plot, size, tabela, nBits, code))
    # Cenário de Alto Ruído Canal Unitário
    porcentagens.append(altoRuidoCanalUnitario.cenario(x, plot, size, tabela, nBits, code))
    # Cenário de Alto Ruído Canal Rayleigh
    porcentagens.append(altoRuidoCanalRayleigh.cenario(x, h1, h2, plot, size, tabela, nBits, code))
    return porcentagens

# Executa os cenários e coleta as porcentagens de acertos
porcentagens = coletar_porcentagens()

# Instancia a classe de plotagem e plota os resultados
plotagem = Plotagem()
if code == 'Golay':
    plotagem.plota_resultados_golay(porcentagens)
else:
    plotagem.plota_resultados_ldpc_bchamming(code, porcentagens, len(x))

# Marca o tempo final e calcula o tempo total de execução
execution_time = time.time() - start_time
hours, rem = divmod(execution_time, 3600)
minutes, seconds = divmod(rem, 60)
print(f"Tempo de execução da simulação: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
