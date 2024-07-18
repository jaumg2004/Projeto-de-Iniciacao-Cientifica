import numpy as np
import random

class Golay:
    def __init__(self):
        self.generator_matrix = self.generate_golay_generator_matrix()
        self.parity_check_matrix = self.generate_parity_check_matrix()

    def generate_golay_generator_matrix(self):
        """
        Gera a matriz geradora do código de Golay (24,12).
        """
        I12 = np.eye(12, dtype=int)  # Matriz identidade 12x12
        P = np.array([
            [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
            [1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1],
            [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
            [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0]
        ], dtype=int)

        G = np.concatenate((I12, P), axis=1)
        return G

    def generate_parity_check_matrix(self):
        """
        Gera a matriz de verificação de paridade (H) para o código de Golay (24,12).
        """
        P = np.array([
            [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
            [1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1],
            [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
            [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0]
        ], dtype=int)

        I12 = np.eye(12, dtype=int)  # Matriz identidade 12x12
        H = np.concatenate((P.T, I12), axis=1)
        return H

    def encode_golay(self, info_word):
        """
        Codifica uma palavra de informação usando o código de Golay.
        """
        codeword = np.dot(info_word, self.generator_matrix) % 2
        return codeword

    def decode_golay(self, received):
        """
        Decodifica uma palavra recebida usando o código de Golay.
        """
        # Calcula a síndrome
        syndrome = np.dot(received, self.parity_check_matrix.T) % 2
        if np.count_nonzero(syndrome) == 0:
            # Nenhum erro detectado, retorna a palavra recebida
            return received

        # Tenta corrigir um erro, se houver
        for i in range(24):
            test_vector = np.zeros(24, dtype=int)
            test_vector[i] = 1
            test_syndrome = np.dot(test_vector, self.parity_check_matrix.T) % 2
            if np.array_equal(syndrome, test_syndrome):
                received[i] = (received[i] + 1) % 2  # Corrige o bit errado
                return received

        # Tenta detectar dois erros
        for i in range(24):
            for j in range(i + 1, 24):
                test_vector = np.zeros(24, dtype=int)
                test_vector[i] = 1
                test_vector[j] = 1
                test_syndrome = np.dot(test_vector, self.parity_check_matrix.T) % 2
                if np.array_equal(syndrome, test_syndrome):
                    # Se encontrar padrão de síndrome correspondente, assume correção
                    received[i] = (received[i] + 1) % 2
                    received[j] = (received[j] + 1) % 2
                    return received

        # Tenta detectar três erros
        for i in range(24):
            for j in range(i + 1, 24):
                for k in range(j + 1, 24):
                    test_vector = np.zeros(24, dtype=int)
                    test_vector[i] = 1
                    test_vector[j] = 1
                    test_vector[k] = 1
                    test_syndrome = np.dot(test_vector, self.parity_check_matrix.T) % 2
                    if np.array_equal(syndrome, test_syndrome):
                        # Se encontrar padrão de síndrome correspondente, assume correção
                        received[i] = (received[i] + 1) % 2
                        received[j] = (received[j] + 1) % 2
                        received[k] = (received[k] + 1) % 2
                        return received

        return received

    def generate_code_table(self):
        """
        Gera a tabela de códigos Golay.
        """
        info_words = [list(map(int, format(i, '012b'))) for i in range(2**12)]
        code_table = [self.encode_golay(info_word) for info_word in info_words]
        return code_table

    def test_golay_key_agreement(self, A_K, B_K, code_table):
        """
        Testa o acordo de chave usando o código de Golay.
        """

        # Converte as strings binárias em listas de inteiros
        A_K = [int(bit) for bit in A_K]
        B_K = [int(bit) for bit in B_K]

        # Alice seleciona uma palavra-código aleatória (c)
        c = random.choice(code_table)

        # Alice calcula s = c XOR A_K
        s = [(c[i] ^ A_K[i]) for i in range(24)]

        # Bob recebe s e calcula c_B = s XOR B_K
        c_B = [(s[i] ^ B_K[i]) for i in range(24)]

        # Bob decodifica c_B para obter c
        c_decoded = self.decode_golay(c_B)

        # Bob calcula A_K_calculated = s XOR c_decoded
        A_K_calculated = [(s[i] ^ c_decoded[i]) for i in range(24)]

        return ''.join(map(str, A_K_calculated))
