import numpy as np
import galois

class BCH:
    def __init__(self, n_bits):
        if n_bits not in [7, 15, 31, 63, 127, 255]:
            raise ValueError("Número de bits não suportado para BCH")

        self.n_bits = n_bits
        # Mapeamento do número de bits de informação
        k = {
            7: 4,
            15: 11,
            31: 26,
            63: 7,
            127: 64,
            255: 123
        }
        self.k_bits = k[self.n_bits]
        self.t = self.get_correction_capacity()  # Capacidade de correção de erros
        self.generator_polynomial = self.get_generator_polynomial()

    def get_correction_capacity(self):
        """
        Retorna a capacidade de correção de erros para o comprimento do código BCH.
        """
        correction_capacities = {
            7: 1,
            15: 1,
            31: 1,
            63: 10,
            127: 10,
            255: 19
        }
        return correction_capacities[self.n_bits]

    def get_generator_polynomial(self):
        """
        Retorna o polinômio gerador calculado para os parâmetros do código BCH.
        """
        # Usar a função BCH do pacote galois para gerar o código com parâmetros (n_bits, k_bits)
        d = 2*self.t + 1# Calculando a dintância miníma de Hamming
        bch_code = galois.BCH(self.n_bits, self.k_bits, d)

        return bch_code.generator_poly

    def encode_bch(self, info_word):
        """
        Codifica uma palavra de informação usando o polinômio gerador do BCH.
        """

        # Criar o objeto BCH do Galois para codificação
        d = 2*self.t + 1
        bch_code = galois.BCH(self.n_bits, self.k_bits, d)

        # Codificar a palavra de informação
        codeword = bch_code.encode(info_word)

        # Retornar a palavra de código codificada
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
            print(f'Código BCH: {''.join(map(str, code_table[i]))}')

        return code_table
