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

    """
    def key_hamming_generation(self, y1, y2, code_table):

        def xor_binary(fc, P):
            assert len(fc) == len(P), "Os valores devem ter o mesmo número de dígitos binários."
            return ''.join('0' if a == b else '1' for a, b in zip(fc, P))

        def hamming_distance(s1, s2):
            length = min(len(s1), len(s2))
            return sum(ch1 != ch2 for ch1, ch2 in zip(s1[:length], s2[:length]))

        def comparacao_mais_proxima(y, tabela):
            min_dist = float('inf')
            pos = -1

            for i, code in enumerate(tabela):
                aux = hamming_distance(y, code)
                if aux < min_dist:
                    pos = i
                    min_dist = aux

            return tabela[pos]

        # Escolhendo uma palavra-código aleatória da tabela
        c = random.choice(code_table)

        # Fazendo uma XOR entre a palavra-código escolhida e a chave A
        s = xor_binary(y1, c)

        # Bob calcula c_B a partir de s e y2
        c_B = xor_binary(s, y2)

        # Calcula a palavra-código mais próxima de c_B na tabela
        c_B_closest = comparacao_mais_proxima(c_B, code_table)

        # Recupera a chave A de Bob
        B_k = xor_binary(s, c_B_closest)

        return B_k
    """


    def encontraErros(self, x, y):
        return sum(1 for i in range(len(x)) if y[i] != x[i])

    def hamming_distance(self, s1, s2):
        length = min(len(s1), len(s2))
        return sum(ch1 != ch2 for ch1, ch2 in zip(s1[:length], s2[:length]))

    def comparacao_mais_proxima(self, y, tabela):
        min_dist = float('inf')
        pos = -1

        for i, code in enumerate(tabela):
            aux = self.hamming_distance(y, code)
            if aux < min_dist:
                pos = i
                min_dist = aux

        return tabela[pos]

    def encontraParidade(self, y, tabela):
        fc = self.comparacao_mais_proxima(y, tabela)
        P = self.subtract_binary(fc, y)
        return P

    def comparaSinais(self, y, P, tabela):
        fc = self.comparacao_mais_proxima(self.subtract_binary(y, P), tabela)
        min_len = min(len(fc), len(P))
        fc_padded = fc[:min_len]
        P_padded = P[:min_len]
        return self.xor_binary(fc_padded, P_padded)

    def subtract_binary(self, fc, y):
        assert len(fc) == len(y), "Os valores devem ter o mesmo número de dígitos binários."
        min_len = min(len(fc), len(y))
        return ''.join('0' if a == b else '1' for a, b in zip(fc[:min_len], y[:min_len]))

    def xor_binary(self, fc, P):
        assert len(fc) == len(P), "Os valores devem ter o mesmo número de dígitos binários."
        return ''.join('0' if a == b else '1' for a, b in zip(fc, P))