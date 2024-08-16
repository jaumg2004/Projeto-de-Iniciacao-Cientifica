import numpy as np
import galois

class BCH:
    def __init__(self, n_bits):
        if n_bits not in [7, 15, 31, 63, 127, 255]:
            raise ValueError("Número de bits não suportado para BCH")

        self.n_bits = n_bits
        self.t = self.get_correction_capacity()  # Capacidade de correção de erros
        self.generator_polynomial = self.get_generator_polynomial()

        # Mapeamento do número de bits de informação
        k = {
            7: 4,
            15: 11,
            31: 21,
            63: 45,
            127: 92,
            255: 123
        }
        self.k_bits = k[self.n_bits]

    def get_correction_capacity(self):
        """
        Retorna a capacidade de correção de erros para o comprimento do código BCH.
        """
        correction_capacities = {
            7: 1,
            15: 2,
            31: 5,
            63: 10,
            127: 21,
            255: 31
        }
        return correction_capacities[self.n_bits]

    def generate_bch_polynomial(self, n, t):
        """
        Calcula o polinômio gerador do código BCH com base no comprimento n e capacidade de correção t.
        """
        m = int(np.log2(n + 1))  # Calcula o valor de m a partir de n

        # Criar o campo de Galois GF(2^m)
        GF = galois.GF(2**m)

        # Definir o elemento primitivo alfa no campo de Galois
        alpha = GF.primitive_element

        # Calcular as raízes usando potências de alpha
        roots = [alpha**i for i in range(1, 2 * t + 1)]

        def min_polynomial(root):
            """
            Calcula o polinômio mínimo de uma raiz específica no campo de Galois.
            """
            root_poly = np.array([1], dtype=int)  # Polinômio inicial [1]

            # Multiplicar (x - raiz) iterativamente
            for _ in range(m):
                # x - root no campo de Galois GF(2)
                root_poly = np.convolve(root_poly, np.array([1, root], dtype=int)) % 2

            return root_poly

        # Começar com o polinômio g(x) = 1
        g_poly = np.array([1], dtype=int)

        # Calcular o produto dos polinômios mínimos para obter g(x)
        for root in roots:
            min_poly = min_polynomial(root)
            g_poly = np.convolve(g_poly, min_poly) % 2

        return g_poly

    def get_generator_polynomial(self):
        """
        Retorna o polinômio gerador calculado para os parâmetros do código BCH.
        """
        return self.generate_bch_polynomial(self.n_bits, self.t)

    def encode_bch(self, info_word):
        """
        Codifica uma palavra de informação usando o polinômio gerador do BCH.
        """
        # Ajustar o polinômio da palavra de informação para x^(n-k)
        message = np.array(info_word, dtype=int)
        message_poly = np.concatenate((message, np.zeros(self.n_bits - self.k_bits, dtype=int)))

        # Divisão do polinômio ajustado pelo polinômio gerador para obter o resto
        generator_poly = self.generator_polynomial
        _, remainder = np.polydiv(message_poly, generator_poly)

        # Parity bits são o resto da divisão polinomial
        parity_bits = np.mod(remainder, 2).astype(int)[-len(generator_poly)+1:]

        # Concatenar info_word com parity_bits para formar a palavra de código completa
        codeword = np.concatenate((message, parity_bits[:(self.n_bits - self.k_bits)])).astype(int)
        if len(codeword) < self.n_bits:
            parity_bits = np.zeros(self.n_bits - self.k_bits, dtype=int)
            parity_bits[-len(remainder):] = remainder[-len(parity_bits):]
            codeword = np.concatenate((message, parity_bits)).astype(int)

        return ''.join(map(str, codeword))

    def generate_code_table(self, size=None):
        """
        Gera uma tabela de códigos para todas as palavras de informação possíveis.
        """
        if size is None:
            size = 2**self.k_bits  # Tamanho padrão para todos os bits suportados

        # Gerar todas as palavras de informação possíveis (vetores de bits)
        info_words = [list(map(int, format(i, f'0{self.k_bits}b'))) for i in range(size)]

        # Codificar cada palavra de informação para obter a tabela de códigos
        code_table = [self.encode_bch(np.array(info_word, dtype=int)) for info_word in info_words]

        return info_words, code_table

    """
    def key_bch_generation(self, y1, y2, code_table):

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
    def key_bch_generation(self, y1, y2, code_table):

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
            min_dist = 2*self.t + 1
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
