from abc import ABC, abstractmethod

class CenárioBase(ABC):
    def __init__(self, media, variancia, ntestes):
        self.media = media
        self.variancia = variancia
        self.ntestes = ntestes

    @abstractmethod
    def cenario(self):
        pass

    @abstractmethod
    def calculaY(self):
        pass

    def encontraErros(self, x, y):
        return sum(1 for i in range(len(x)) if y[i] != x[i])

    def comparacao_mais_proxima(self, y, tabela):
        def hamming_distance(s1, s2):
            length = min(len(s1), len(s2))
            return sum(ch1 != ch2 for ch1, ch2 in zip(s1[:length], s2[:length]))

        min_dist = float('inf')
        pos = -1

        for i, code in enumerate(tabela):
            aux = hamming_distance(y, code)
            if aux < min_dist:
                pos = i
                min_dist = aux

        return tabela[pos]

    def encontraParidade(self, y, tabela):
        max_length = len(bin(max(y))) - 2
        y_str = ''.join(format(i, f'0{max_length}b') for i in y)
        fc = self.comparacao_mais_proxima(y_str, tabela)
        P = self.subtract_binary(fc, y_str)
        return P

    def subtract_binary(self, fc, y):
        min_len = min(len(fc), len(y))
        return ''.join('0' if a == b else '1' for a, b in zip(fc[:min_len], y[:min_len]))

    def xor_binary(self, fc, P):
        assert len(fc) == len(P), "Os valores devem ter o mesmo número de dígitos binários."
        return ''.join('0' if a == b else '1' for a, b in zip(fc, P))

    def comparaSinais(self, y, P, tabela):
        y_str = ''.join(map(str, y))
        fc = self.comparacao_mais_proxima(self.subtract_binary(y_str, P), tabela)
        min_len = min(len(fc), len(P))
        fc_padded = fc[:min_len]
        P_padded = P[:min_len]
        return self.xor_binary(fc_padded, P_padded)

