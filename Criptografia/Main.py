import time
import numpy as np
import random

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

x = []
x_bchamming = []
x_golay = []

h1 = []
h2 = []

# Solicita ao usuário a quantidade de testes
ntestes = int(input("Entre com a quantidade de testes: "))

print("Entre com um dos valores possiveis para o tamanho da cadeia de Bits")
nBits = int(input("7 Bits, 15 Bits, 31 Bits, 63 Bits, 127 Bits ou 255 Bits\n"))
if nBits > 15:
    size = int(input("Entre com tamanho do espaço amostral: "))
else:
    size = None

# Gera uma lista de bits aleatórios (0 ou 1)
for i in range(24):
    x_golay.append(random.randint(0, 1))

for i in range(nBits):
    x_bchamming.append(random.randint(0, 1))

x.append(x_bchamming)
x.append(x_golay)

h1_bchamming = np.random.rayleigh(1.0, nBits)
h2_bchamming = np.random.rayleigh(1.0, nBits)

h1_golay = np.random.rayleigh(1.0, 24)
h2_golay = np.random.rayleigh(1.0, 24)

h1.append(h1_bchamming)
h1.append(h1_golay)

h2.append(h2_bchamming)
h2.append(h2_golay)

comando = input("Deseja realizar a Plotagem dos sinais? 'y' para sim, 'n' para nao ")
if comando == 'y':
    plot = 1
else:
    plot = 0

ruidoNuloCanalUnitario = RuidoNuloCanalUnitario(media, variancia, ntestes)
baixoRuidoCanalUnitario = BaixoRuidoCanalUnitario(media, variancia, ntestes)
baixoRuidoCanalRayleigh = BaixoRuidoCanalRayleigh(media, variancia, ntestes)
altoRuidoCanalUnitario = AltoRuidoCanalUnitario(media, variancia, ntestes)
altoRuidoCanalRayleigh = AltoRuidoCanalRayleigh(media, variancia, ntestes)


def coletar_porcentagens():
    porcentagens_hamming = []
    porcentagens_bch = []
    porcentagens_ldpc = []
    porcentagens_golay = []

    # Cenário de Ruido Nulo Canal Unitário
    hamming_ruido_nulo = ruidoNuloCanalUnitario.cenario(x, nBits, plot, size)
    porcentagens_hamming.append(hamming_ruido_nulo[0])  # Porcentagem de Hamming
    porcentagens_bch.append(hamming_ruido_nulo[1])  # Porcentagem de BCH
    porcentagens_ldpc.append(hamming_ruido_nulo[2])  # Porcentagem de LDPC
    porcentagens_golay.append(hamming_ruido_nulo[3])  # Porcentagem de Golay

    # Cenário de Baixo Ruído Canal Unitário
    hamming_baixo_ruido = baixoRuidoCanalUnitario.cenario(x, nBits, plot, size)
    porcentagens_hamming.append(hamming_baixo_ruido[0])
    porcentagens_bch.append(hamming_baixo_ruido[1])
    porcentagens_ldpc.append(hamming_baixo_ruido[2])
    porcentagens_golay.append(hamming_baixo_ruido[3])

    # Cenário de Baixo Ruído Canal Rayleigh
    hamming_baixo_rayleigh = baixoRuidoCanalRayleigh.cenario(x, h1, h2, nBits, plot, size)
    porcentagens_hamming.append(hamming_baixo_rayleigh[0])
    porcentagens_bch.append(hamming_baixo_rayleigh[1])
    porcentagens_ldpc.append(hamming_baixo_rayleigh[2])
    porcentagens_golay.append(hamming_baixo_rayleigh[3])

    # Cenário de Alto Ruído Canal Unitário
    hamming_alto_ruido = altoRuidoCanalUnitario.cenario(x, nBits, plot, size)
    porcentagens_hamming.append(hamming_alto_ruido[0])
    porcentagens_bch.append(hamming_alto_ruido[1])
    porcentagens_ldpc.append(hamming_alto_ruido[2])
    porcentagens_golay.append(hamming_alto_ruido[3])

    # Cenário de Alto Ruído Canal Rayleigh
    hamming_alto_rayleigh = altoRuidoCanalRayleigh.cenario(x, h1, h2, nBits, plot, size)
    porcentagens_hamming.append(hamming_alto_rayleigh[0])
    porcentagens_bch.append(hamming_alto_rayleigh[1])
    porcentagens_ldpc.append(hamming_alto_rayleigh[2])
    porcentagens_golay.append(hamming_alto_rayleigh[3])

    return porcentagens_hamming, porcentagens_bch, porcentagens_ldpc, porcentagens_golay

# Executa os cenários e coleta as porcentagens de acertos
porcentagens_hamming, porcentagens_bch, porcentagens_ldpc, porcentagens_golay = coletar_porcentagens()

# Instancia a classe de plotagem
plotagem = Plotagem()

# Plota os resultados
plotagem.plota_resultados_ldpc_bchamming(porcentagens_hamming, porcentagens_bch, porcentagens_ldpc, nBits)
plotagem.plota_resultados_golay(porcentagens_golay)

# Marca o tempo final
end_time = time.time()

# Marca o tempo final e calcula o tempo total de execução
end_time = time.time()
execution_time = end_time - start_time

# Calcula horas, minutos e segundos
hours, rem = divmod(execution_time, 3600)
minutes, seconds = divmod(rem, 60)

# Exibe o tempo de execução formatado
print(f"Tempo de execução: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
