import numpy as np
from pyldpc import make_ldpc

class LDPC:
    def __init__(self, n_bits):
        if n_bits not in [7, 15, 31, 63, 127, 255]:
            raise ValueError("Número de bits não suportado para LDPC")

        self.n_bits = n_bits
        self.H, self.G = self.get_ldpc_matrices()
        self.k_bits = self.G.shape[1]  # Número de bits de informação

    def binaryproduct(self, X, Y):
        """Compute a matrix-matrix / vector product in Z/2Z."""
        A = X.dot(Y)
        try:
            A = A.toarray()
        except AttributeError:
            pass
        return A % 2

    def get_ldpc_matrices(self):
        """
        Gera as matrizes de paridade (H) e geradora (G) para o código LDPC.
        """
        d_v = {7: 4, 15: 4, 31: 10, 63: 6, 127: 5, 255: 15}
        d_c = {7: 7, 15: 5, 31: 31, 63: 21, 127: 127, 255: 255}

        dv_value = d_v.get(self.n_bits)
        dc_value = d_c.get(self.n_bits)

        # Gera as matrizes H e G usando valores de dv e dc
        H, G = make_ldpc(self.n_bits, dv_value, dc_value, systematic=True, sparse=True)

        return H, G

    def encode_ldpc(self, info_word):
        """
        Codifica uma palavra de informação usando a matriz geradora G do LDPC.
        """
        codeword = self.binaryproduct(self.G, np.array(info_word, dtype=int))
        return ''.join(map(str, codeword))

    def generate_code_table(self, size=None):
        """
        Gera uma tabela de códigos para todas as palavras de informação possíveis.
        """
        if size is None:
            size = 2**self.k_bits  # Tamanho padrão para todos os bits suportados

        info_words = [list(map(int, format(i, f'0{self.k_bits}b'))) for i in range(size)]
        code_table = [self.encode_ldpc(info_word) for info_word in info_words]

        for i in range(len(info_words)):
            print(f'Código LDPC: {code_table[i]}')

        return code_table
