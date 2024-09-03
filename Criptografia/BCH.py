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
            127: 120,
            255: 123
        }
        self.k_bits = k[self.n_bits]

    def get_correction_capacity(self):
        """
        Retorna a capacidade de correção de erros para o comprimento do código BCH.
        """
        correction_capacities = {
            7: 1,
            15: 1,
            31: 5,
            63: 3,
            127: 1,
            255: 21
        }
        return correction_capacities[self.n_bits]

    def generate_bch_polynomial(self, n, t):
        """
        Calcula o polinômio gerador do código BCH com base no comprimento n e capacidade de correção t.
        """
        m = int(np.log2(n + 1))  # Calcula o valor de m a partir de n

        # Criar o campo de Galois GF(2^m)
        GF = galois.GF(2**m)
        print(GF)

        # Definir o elemento primitivo alfa no campo de Galois
        alpha = GF.primitive_element
        print(alpha)

        # Calcular as raízes usando potências de alpha
        roots = [alpha**i for i in range(1, 2 * t + 1)]
        print(roots)

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

        for i in range(len(info_words)):
            print(f'Código: {''.join(map(str, code_table[i]))}')

        return code_table
