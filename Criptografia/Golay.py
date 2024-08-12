import random

import numpy as np

class Golay:
    def __init__(self):
        self.generator_matrix = self.generate_golay_generator_matrix()

    def generate_golay_generator_matrix(self):
        """
        Gera a matriz geradora do código de Golay (24,12).
        """
        I12 = np.eye(12, dtype=int)  # Matriz identidade 12x12
        P = np.random.randint(0, 2, (12, 12), dtype=int)  # Matriz aleatória 12x12

        G = np.concatenate((I12, P), axis=1)

        return G

    def encode_golay(self, info_word):
        """
        Codifica uma palavra de informação usando o código de Golay.
        """
        codeword = np.dot(info_word, self.generator_matrix) % 2
        return ''.join(map(str, codeword))

    def generate_code_table(self):
        """
        Gera a tabela de códigos Golay.
        """
        info_words = [list(map(int, format(i, '012b'))) for i in range(2**12)]
        code_table = [self.encode_golay(info_word) for info_word in info_words]
        print("Tabela de Código Golay:")
        for i in range(len(info_words)):
            print(f"Informação: {''.join(map(str, info_words[i]))} -> Código: {''.join(map(str, code_table[i]))}")

        return code_table

    """
    def key_golay_generation(self, y1, y2, code_table):

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
        A_k = xor_binary(s, c_B_closest)

        return A_k
    """

    """
    def key_golay_generation(self, y1, y2, code_table):

        def subtract_binary(fc, y):
            assert len(fc) == len(y), "Os valores devem ter o mesmo número de dígitos binários."
            min_len = min(len(fc), len(y))
            return ''.join('0' if a == b else '1' for a, b in zip(fc[:min_len], y[:min_len]))

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

        def encontraParidade(y, tabela):
            fc = comparacao_mais_proxima(y, tabela)
            P = subtract_binary(fc, y)
            return P

        def comparaSinais(y, P, tabela):
            fc = comparacao_mais_proxima(subtract_binary(y, P), tabela)
            min_len = min(len(fc), len(P))
            fc_padded = fc[:min_len]
            P_padded = P[:min_len]
            return xor_binary(fc_padded, P_padded)

        return comparaSinais(y2, encontraParidade(y1, code_table), code_table)
    """