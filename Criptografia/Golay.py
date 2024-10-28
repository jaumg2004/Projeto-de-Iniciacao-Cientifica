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
            print(f'Código Golay: {''.join(map(str, code_table[i]))}')

        return code_table

