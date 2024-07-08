import numpy as np
import random

# Classes dos canais
from Cenário1 import RuidoNuloCanalUnitario
from Cenário2 import BaixoRuidoCanalUnitario
from Cenário3 import BaixoRuidoCanalRayleigh
from Cenário4 import AltoRuidoCanalUnitario
from Cenário5 import AltoRuidoCanalRayleigh

#Classe de plotagem
from Plotagem import Plotagem

# Variáveis globais
media = 0.5
variancia = 1.5

x = []

# Solicita ao usuário a quantidade de testes
ntestes = int(input("Entre com a quantidade de testes: "))

print("Entre com um dos valores possiveis para o tamanho da cadeia de Bits")
nBits = int(input("7 Bits, 15 Bits, 31 Bits, 63 Bits,127 Bits ou 255 Bits\n"))

# Gera uma lista de bits aleatórios (0 ou 1)
for i in range(nBits):
    x.append(random.randint(0, 1))

h1 = np.random.rayleigh(1.0, nBits)
h2 = np.random.rayleigh(1.0, nBits)

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
    porcentagens = []
    porcentagens.append(ruidoNuloCanalUnitario.cenario(x, nBits, plot))
    porcentagens.append(baixoRuidoCanalUnitario.cenario(x, nBits, plot))
    porcentagens.append(baixoRuidoCanalRayleigh.cenario(x, h1, h2, nBits, plot))
    porcentagens.append(altoRuidoCanalUnitario.cenario(x, nBits, plot))
    porcentagens.append(altoRuidoCanalRayleigh.cenario(x, h1, h2, nBits, plot))
    return porcentagens

# Executa os cenários e coleta as porcentagens de acertos
porcentagens = coletar_porcentagens()

# Instancia a classe de plotagem
plotagem = Plotagem()

# Plota os resultados
plotagem.plota_resultados(porcentagens)


