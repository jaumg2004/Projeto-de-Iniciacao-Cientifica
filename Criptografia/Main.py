import time
import numpy as np
import random

# Classes das tabelas
from Hamming import Hamming
from BCH import BCH
from Golay import Golay
from LDPC import LDPC

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
x_golay = [random.randint(0, 1) for _ in range(24)]
x_bchamming = [random.randint(0, 1) for _ in range(nBits)]
x = [x_bchamming, x_golay]

# Amostras de canais de Rayleigh
h1 = [np.random.rayleigh(1.0, nBits), np.random.rayleigh(1.0, 24)]
h2 = [np.random.rayleigh(1.0, nBits), np.random.rayleigh(1.0, 24)]

# Verifica se o usuário deseja a plotagem
comando = input("Deseja realizar a Plotagem dos sinais? 'y' para sim, 'n' para nao \n")
plot = 1 if comando == 'y' else 0

# Inicializa tabelas de códigos de correção
tabelas = []

# Gera as tabelas de códigos para cada método

hamming = Hamming()
if nBits == 7:
    tabelas.append(['0000000', '1101001', '0101010', '1000011', '1001100', '0100101', '1100110', '0001111',
                    '1110000', '0011001', '1011010', '0110011', '0111100', '1010101', '0010110', '1111111'])
elif nBits == 15:
    tabelas.append(hamming.generate_hamming_codes_15_bits())
elif nBits == 31:
    tabelas.append(hamming.generate_space_amostral_sample_31_bits(size))
elif nBits == 63:
    tabelas.append(hamming.generate_space_amostral_sample_63_bits(size))
elif nBits == 127:
    tabelas.append(hamming.generate_space_amostral_sample_127_bits(size))
elif nBits == 255:
    tabelas.append(hamming.generate_space_amostral_sample_255_bits(size))
else:
    raise ValueError("Número de bits não suportado")

bch = BCH(nBits)
tabelas.append(bch.generate_code_table(size))

ldpc = LDPC(nBits)
tabelas.append(ldpc.generate_code_table(size))

golay = Golay()
tabelas.append(golay.generate_code_table())

print(tabelas[0])

# Inicializa canais de comunicação
ruidoNuloCanalUnitario = RuidoNuloCanalUnitario(media, variancia, ntestes)
baixoRuidoCanalUnitario = BaixoRuidoCanalUnitario(media, variancia, ntestes)
baixoRuidoCanalRayleigh = BaixoRuidoCanalRayleigh(media, variancia, ntestes)
altoRuidoCanalUnitario = AltoRuidoCanalUnitario(media, variancia, ntestes)
altoRuidoCanalRayleigh = AltoRuidoCanalRayleigh(media, variancia, ntestes)


def coletar_porcentagens():
    porcentagens_hamming, porcentagens_bch, porcentagens_ldpc, porcentagens_golay = [], [], [], []

    # Cenário de Ruído Nulo Canal Unitário
    hamming_ruido_nulo = ruidoNuloCanalUnitario.cenario(x, nBits, plot, size, tabelas)
    porcentagens_hamming.append(hamming_ruido_nulo[0])
    porcentagens_bch.append(hamming_ruido_nulo[1])
    porcentagens_ldpc.append(hamming_ruido_nulo[2])
    porcentagens_golay.append(hamming_ruido_nulo[3])

    # Cenário de Baixo Ruído Canal Unitário
    hamming_baixo_ruido = baixoRuidoCanalUnitario.cenario(x, nBits, plot, size, tabelas)
    porcentagens_hamming.append(hamming_baixo_ruido[0])
    porcentagens_bch.append(hamming_baixo_ruido[1])
    porcentagens_ldpc.append(hamming_baixo_ruido[2])
    porcentagens_golay.append(hamming_baixo_ruido[3])

    # Cenário de Baixo Ruído Canal Rayleigh
    hamming_baixo_rayleigh = baixoRuidoCanalRayleigh.cenario(x, h1, h2, nBits, plot, size, tabelas)
    porcentagens_hamming.append(hamming_baixo_rayleigh[0])
    porcentagens_bch.append(hamming_baixo_rayleigh[1])
    porcentagens_ldpc.append(hamming_baixo_rayleigh[2])
    porcentagens_golay.append(hamming_baixo_rayleigh[3])

    # Cenário de Alto Ruído Canal Unitário
    hamming_alto_ruido = altoRuidoCanalUnitario.cenario(x, nBits, plot, size, tabelas)
    porcentagens_hamming.append(hamming_alto_ruido[0])
    porcentagens_bch.append(hamming_alto_ruido[1])
    porcentagens_ldpc.append(hamming_alto_ruido[2])
    porcentagens_golay.append(hamming_alto_ruido[3])

    # Cenário de Alto Ruído Canal Rayleigh
    hamming_alto_rayleigh = altoRuidoCanalRayleigh.cenario(x, h1, h2, nBits, plot, size, tabelas)
    porcentagens_hamming.append(hamming_alto_rayleigh[0])
    porcentagens_bch.append(hamming_alto_rayleigh[1])
    porcentagens_ldpc.append(hamming_alto_rayleigh[2])
    porcentagens_golay.append(hamming_alto_rayleigh[3])

    return porcentagens_hamming, porcentagens_bch, porcentagens_ldpc, porcentagens_golay

# Executa os cenários e coleta as porcentagens de acertos
porcentagens_hamming, porcentagens_bch, porcentagens_ldpc, porcentagens_golay = coletar_porcentagens()

# Instancia a classe de plotagem e plota os resultados
plotagem = Plotagem()
plotagem.plota_resultados_ldpc_bchamming(porcentagens_hamming, porcentagens_bch, porcentagens_ldpc, nBits)
plotagem.plota_resultados_golay(porcentagens_golay)

# Marca o tempo final e calcula o tempo total de execução
execution_time = time.time() - start_time

# Exibe o tempo de execução formatado
hours, rem = divmod(execution_time, 3600)
minutes, seconds = divmod(rem, 60)
print(f"Tempo de execução: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
