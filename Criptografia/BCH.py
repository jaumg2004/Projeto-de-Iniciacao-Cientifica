import random

# Classe BCH
class BCH:
    def __init__(self, n_bits):
        if n_bits not in [7, 15, 31, 63, 127, 255]:
            raise ValueError("Número de bits não suportado para BCH")

        self.n_bits = n_bits
        self.generator_matrix = self.generate_bch_generator_matrix()

    def generate_bch_generator_matrix(self):
        return [[random.randint(0, 1) for _ in range(self.n_bits)] for _ in range(self.n_bits)]

    def xor_vectors(self, v1, v2):
        return [(a ^ b) for a, b in zip(v1, v2)]

    def generate_code_table(self, size):
        if size is None:
            size = 2**self.n_bits  # Tamanho padrão para todos os bits suportados

        info_words = [[int(bit) for bit in format(i, f'0{self.n_bits}b')] for i in range(size)]
        code_table = [self.encode_bch(info_word) for info_word in info_words]
        return code_table

    def encode_bch(self, info_word):
        codeword = []
        for row in self.generator_matrix:
            bit = sum(info_word[j] & row[j] for j in range(self.n_bits)) % 2
            codeword.append(bit)
        return codeword

    def decode_bch(self, received, code_table):
        def hamming_distance(v1, v2):
            return sum(a != b for a, b in zip(v1, v2))

        min_distance = float('inf')
        closest_codeword = None

        for candidate in code_table:
            distance = hamming_distance(received, candidate)

            if distance < min_distance:
                min_distance = distance
                closest_codeword = candidate

            if min_distance == 0:
                break

        return closest_codeword

    def test_bch_key_agreement(self, A_K, B_K, code_table):

        # Converte as strings binárias em listas de inteiros
        A_K = [int(bit) for bit in A_K]
        B_K = [int(bit) for bit in B_K]

        # Alice seleciona uma palavra-código aleatória (c)
        c = random.choice(code_table)

        # Alice calcula s = c XOR A_K
        s = self.xor_vectors(c, A_K)

        # Bob recebe s e calcula c_B = s XOR B_K
        c_B = self.xor_vectors(s, B_K)

        # Bob decodifica c_B para obter c
        c_decoded = self.decode_bch(c_B, code_table)

        # Bob calcula A_K_calculated = s XOR c_decoded
        A_K_calculated = self.xor_vectors(s, c_decoded)

        return ''.join(map(str, A_K_calculated))


