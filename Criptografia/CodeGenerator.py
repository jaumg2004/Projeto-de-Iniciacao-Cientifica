import numpy as np
import galois
import random
from pyldpc import make_ldpc

class CodeGenerator:
    def __init__(self, n_bits, code):
        self.n_bits = n_bits
        self.code = code
        self.G = self.create_generator_matrix()
        self.k_bits = self.k_bits_size()

    def k_bits_size(self):
        """Retorna o valor de k (número de bits de informação) para o código especificado."""
        if self.code == 'BCH':
            k = {
                7: 4,
                15: 5,
                127: 64,
                255: 247
            }
            return k.get(self.n_bits, None)  # Retorna None se o valor de n_bits não for encontrado

        elif self.code == 'Hamming':
            return self.n_bits - int(np.log2(self.n_bits + 1))

        elif self.code == 'Golay':
            return 12

        elif self.code == "LDPC" and self.G is not None:
            return self.G.T.shape[1]  # Supondo que G já foi inicializado

        return None  # Retorna None explicitamente se o código não for encontrado

    def create_generator_matrix(self):
        """Cria a matriz geradora com base no tipo de código escolhido."""
        generator_creators = {
            'Hamming': self.create_hamming_matrix,
            'LDPC': self.create_ldpc_matrix,
            'Golay': self.create_golay_matrix
        }
        return generator_creators.get(self.code, lambda: None)()

    def create_hamming_matrix(self):
        """Cria a matriz geradora para o código Hamming."""
        if self.n_bits == 7:
            G = np.array([[1, 0, 0, 0, 1, 0, 1],
                          [0, 1, 0, 0, 1, 1, 1],
                          [0, 0, 1, 0, 1, 1, 0],
                          [0, 0, 0, 1, 0, 1, 1]])
            return G

        # Inicializa a matriz de paridade H (m x n)
        H = np.zeros((int(np.log2(self.n_bits + 1)), self.n_bits), dtype=int)

        # Preenche H com colunas que representam os índices em binário
        for i in range(1, self.n_bits + 1):
            binary_repr = [int(bit) for bit in f"{i:0{int(np.log2(self.n_bits + 1))}b}"]
            H[:, i - 1] = binary_repr

        # Extrai a matriz P (m x k) da transposta de H
        P = H[:, :(self.n_bits - int(np.log2(self.n_bits + 1)))].T

        # Cria a matriz identidade (k x k)
        I_k = np.eye(self.n_bits - int(np.log2(self.n_bits + 1)), dtype=int)

        # Monta a matriz geradora G (k x n)
        G = np.hstack((I_k, P))
        return G

    def create_ldpc_matrix(self):
        """Cria a matriz geradora para o código LDPC."""
        d_v = {7: 6, 15: 4, 127: 126, 255: 200}
        d_c = {7: 7, 15: 5, 127: 127, 255: 255}

        dv_value = d_v.get(self.n_bits)
        dc_value = d_c.get(self.n_bits)
        if dv_value is None or dc_value is None:
            raise ValueError(f"Valores de d_v ou d_c não definidos para n_bits={self.n_bits}")

        _, G = make_ldpc(self.n_bits, dv_value, dc_value, systematic=True, sparse=True)
        return G.T

    def create_golay_matrix(self):
        """Cria a matriz geradora para o código Golay (24, 12)."""
        I12 = np.eye(12, dtype=int)
        P = np.random.randint(0, 2, (12, 12), dtype=int)  # Matriz aleatória 12x12

        return np.concatenate((I12, P), axis=1)

    @staticmethod
    def binary_product(X, Y):
        """Calcula o produto de uma matriz e vetor no campo binário."""
        A = X.dot(Y)
        try:
            A = A.toarray()
        except AttributeError:
            pass
        return A % 2

    def encode_bch(self, info_word):
        """Codifica uma palavra de informação usando o código BCH."""
        t = {7: 1, 15: 3, 127: 10, 255: 1}
        d = 2 * t.get(self.n_bits, 0) + 1
        bch_code = galois.BCH(self.n_bits, self.k_bits, d)
        return ''.join(map(str, bch_code.encode(info_word)))

    def encode(self, info_word):
        """Codifica uma palavra de informação usando a matriz geradora G do código."""
        info_word = np.array(info_word, dtype=int)
        codeword = self.binary_product(self.G.T, info_word)
        return ''.join(map(str, codeword))

    def generate_code_table(self, size=None):
        """Gera uma tabela de códigos para todas as palavras de informação possíveis."""
        if size is None:
            size = 2 ** self.k_bits

        if self.n_bits > 15:
            info_words = [list(map(int, format(random.randint(0, 2**self.k_bits - 1), f'0{self.k_bits}b'))) for _ in range(size)]

        elif self.n_bits <= 15:
            info_words = [list(map(int, format(i, f'0{self.k_bits}b'))) for i in range(size)]

        encoder = self.encode_bch if self.code == 'BCH' else self.encode
        code_table = [encoder(info_word) for info_word in info_words]

        for codeword in code_table:
            print(f'Código {self.code}: {codeword}')
        return code_table
