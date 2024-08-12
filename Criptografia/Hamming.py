import random

class Hamming:
    def __init__(self):
        pass

    def calcular_bits_paridade(self, binary_pattern, positions):
        parity_bits = ''
        for pos in positions:
            sum_bits = sum(int(binary_pattern[i]) for i in pos)
            parity_bits += str(sum_bits % 2)
        return parity_bits

    def gerar_codigos_hamming(self, tamanho_informacao, posicoes_paridade):
        codigos_hamming = []
        for i in range(2 ** tamanho_informacao):
            padrao_binario = format(i, f'0{tamanho_informacao}b')
            bits_paridade = self.calcular_bits_paridade(padrao_binario, posicoes_paridade)
            codigo_hamming = padrao_binario + bits_paridade
            codigos_hamming.append(codigo_hamming)
        return codigos_hamming

    def gerar_codigo_hamming(self, tamanho_informacao, posicoes_paridade, add_zero_bit=False):
        padrao_binario = format(random.randint(0, 2 ** tamanho_informacao - 1), f'0{tamanho_informacao}b')
        bits_paridade = self.calcular_bits_paridade(padrao_binario, posicoes_paridade)
        codigo_hamming = padrao_binario + bits_paridade
        if add_zero_bit:
            codigo_hamming += '0'
        return codigo_hamming

    def gerar_espaco_amostral(self, tamanho_informacao, posicoes_paridade, size, add_zero_bit=False):
        espaco_amostral = []
        for _ in range(size):
            codigo_hamming = self.gerar_codigo_hamming(tamanho_informacao, posicoes_paridade, add_zero_bit)
            espaco_amostral.append(codigo_hamming)
        return espaco_amostral

    def generate_hamming_codes_15_bits(self):
        posicoes_paridade = [(0, 1, 3), (0, 2, 3), (1, 2, 3), (4, 5, 6, 7, 8, 9, 10)]
        return self.gerar_codigos_hamming(11, posicoes_paridade)

    def generate_space_amostral_sample_31_bits(self, size):
        posicoes_paridade = [(0, 1, 3), (0, 2, 3), (1, 2, 3), (4, 5, 6, 7, 8, 9, 10)]
        return self.gerar_espaco_amostral(26, posicoes_paridade, size, add_zero_bit=True)

    def generate_space_amostral_sample_63_bits(self, size):
        posicoes_paridade = [
            range(0, 8, 2), range(0, 8, 4), range(1, 8, 4), range(0, 16, 8),
            range(0, 32, 16), range(0, 64, 32)
        ]
        return self.gerar_espaco_amostral(57, posicoes_paridade, size)

    def generate_space_amostral_sample_127_bits(self, size):
        posicoes_paridade = [
            range(0, 16, 2), range(0, 16, 4), range(0, 32, 4), range(0, 32, 8),
            range(0, 64, 8), range(0, 64, 16), range(0, 128, 16)
        ]
        return self.gerar_espaco_amostral(120, posicoes_paridade, size)

    def generate_space_amostral_sample_255_bits(self, size):
        posicoes_paridade = [
            range(0, 32, 2), range(0, 32, 4), range(0, 64, 4), range(0, 64, 8),
            range(0, 128, 8), range(0, 128, 16), range(0, 256, 16), range(0, 256, 32)
        ]
        return self.gerar_espaco_amostral(247, posicoes_paridade, size)


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
        A_k = xor_binary(s, c_B_closest)

        return A_k


    """
    def key_hamming_generation(self, y1, y2, code_table):

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

