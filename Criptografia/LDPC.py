import numpy as np
from scipy.sparse import csr_matrix

class LDPC:
    def __init__(self, n_bits):
        if n_bits not in [7, 15, 31, 63, 127, 255]:
            raise ValueError("Número de bits não suportado para LDPC")

        self.n_bits = n_bits
        self.H, self.G = self.get_ldpc_matrices()  # Gera as matrizes H e G para LDPC
        self.k_bits = self.G.shape[1]  # Número de bits de informação

    def gaussjordan(self, X, change=0):
        """Calcule a forma escalonada por linhas binária reduzida de X.

        Parâmetros
        ----------
        X: matriz (m, n)
        change : booleano (True, False). Se True, retorna a transformação inversa

        Retornos
        -------
        if `change` == 'True':
            A: matriz (m, n). Forma escalonada por linhas reduzida de X.
            P: transformações aplicadas à identidade.
        else:
            A: matriz (m, n). Forma escalonada por linhas reduzida de X.

        """
        A = np.copy(X)
        m, n = A.shape

        if change:
            P = np.identity(m).astype(int)

        pivot_old = -1
        for j in range(n):
            filtre_down = A[pivot_old+1:m, j]
            pivot = np.argmax(filtre_down)+pivot_old+1

            if A[pivot, j]:
                pivot_old += 1
                if pivot_old != pivot:
                    aux = np.copy(A[pivot, :])
                    A[pivot, :] = A[pivot_old, :]
                    A[pivot_old, :] = aux
                    if change:
                        aux = np.copy(P[pivot, :])
                        P[pivot, :] = P[pivot_old, :]
                        P[pivot_old, :] = aux

                for i in range(m):
                    if i != pivot_old and A[i, j]:
                        if change:
                            P[i, :] = abs(P[i, :]-P[pivot_old, :])
                        A[i, :] = abs(A[i, :]-A[pivot_old, :])

            if pivot_old == m-1:
                break

        if change:
            return A, P
        return A


    def parity_check_matrix_fixed(self, n_code, d_v, d_c):
        """
        Build a regular Parity-Check Matrix H following a fixed, deterministic pattern.
        """
        if d_v <= 1:
            raise ValueError("d_v must be at least 2.")
        if d_c <= d_v:
            raise ValueError("d_c must be greater than d_v.")
        if n_code % d_c:
            raise ValueError("d_c must divide n for a regular LDPC matrix H.")

        n_equations = (n_code * d_v) // d_c
        block = np.zeros((n_equations // d_v, n_code), dtype=int)
        H = np.empty((n_equations, n_code), dtype=int)
        block_size = n_equations // d_v

        # Filling the first block with consecutive ones in each row of the block
        for i in range(block_size):
            for j in range(i * d_c, (i + 1) * d_c):
                block[i, j] = 1
        H[:block_size] = block

        # Filling the remaining blocks without random permutation (deterministic)
        for i in range(1, d_v):
            for j in range(n_code):
                H[i * block_size: (i + 1) * block_size, j] = block[(i + j) % block_size, j]

        return H

    def coding_matrix_fixed(self, H, sparse=True):
        """Return the generating coding matrix G given the LDPC matrix H, without randomness."""
        if type(H) == csr_matrix:
            H = H.toarray()

        n_equations, n_code = H.shape

        # DOUBLE GAUSS-JORDAN:
        # Assuming 'utils.gaussjordan' is a utility function you have or should define

        Href_colonnes, tQ = self.gaussjordan(H.T, 1)

        Href_diag = self.gaussjordan(np.transpose(Href_colonnes))

        Q = tQ.T

        n_bits = n_code - Href_diag.sum()

        Y = np.zeros(shape=(n_code, n_bits), dtype=int)
        Y[n_code - n_bits:, :] = np.identity(n_bits)

        if sparse:
            Q = csr_matrix(Q)
            Y = csr_matrix(Y)

        tG = self.binaryproduct(Q, Y)

        return tG

    def coding_matrix_systematic_fixed(self, H, sparse=True):
        """Compute a coding matrix G in systematic format with an identity block, without randomness."""
        n_equations, n_code = H.shape

        P1 = np.identity(n_code, dtype=int)

        Hrowreduced = self.gaussjordan(H)

        n_bits = n_code - sum([a.any() for a in Hrowreduced])

        while(True):
            zeros = [i for i in range(min(n_equations, n_code)) if not Hrowreduced[i, i]]
            if len(zeros):
                indice_colonne_a = min(zeros)
            else:
                break
            list_ones = [j for j in range(indice_colonne_a + 1, n_code) if Hrowreduced[indice_colonne_a, j]]
            if len(list_ones):
                indice_colonne_b = min(list_ones)
            else:
                break
            aux = Hrowreduced[:, indice_colonne_a].copy()
            Hrowreduced[:, indice_colonne_a] = Hrowreduced[:, indice_colonne_b]
            Hrowreduced[:, indice_colonne_b] = aux

            aux = P1[:, indice_colonne_a].copy()
            P1[:, indice_colonne_a] = P1[:, indice_colonne_b]
            P1[:, indice_colonne_b] = aux

        P1 = P1.T
        identity = list(range(n_code))
        sigma = identity[n_code - n_bits:] + identity[:n_code - n_bits]

        P2 = np.zeros(shape=(n_code, n_code), dtype=int)
        P2[identity, sigma] = np.ones(n_code)

        if sparse:
            P1 = csr_matrix(P1)
            P2 = csr_matrix(P2)
            H = csr_matrix(H)

        P = self.binaryproduct(P2, P1)

        if sparse:
            P = csr_matrix(P)

        H_new = self.binaryproduct(H, np.transpose(P))

        G_systematic = np.zeros((n_bits, n_code), dtype=int)
        G_systematic[:, :n_bits] = np.identity(n_bits)
        G_systematic[:, n_bits:] = (Hrowreduced[:n_code - n_bits, n_code - n_bits:]).T

        return H_new, G_systematic.T

    def make_ldpc_fixed(self, n_code, d_v, d_c, systematic=False, sparse=True):
        """Create an LDPC coding and decoding matrices H and G with fixed values."""
        H = self.parity_check_matrix_fixed(n_code, d_v, d_c)
        if systematic:
            H, G = self.coding_matrix_systematic_fixed(H, sparse=sparse)
        else:
            G = self.coding_matrix_fixed(H, sparse=sparse)
        return H, G

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
        d_v = {
            7: 4,
            15: 4,
            31: 10,
            63: 6,
            127: 5,
            255: 5
        }  # Grau variável (número de 1s por linha na matriz H)

        d_c = {
            7: 7,
            15: 15,
            31: 31,
            63: 21,
            127: 127,
            255: 51
        }  # Grau de verificação (número de 1s por coluna na matriz H)

        # Seleciona os valores de d_v e d_c correspondentes ao número de bits n_bits
        dv_value = d_v.get(self.n_bits, 4)  # Valor padrão de 4 caso não esteja definido
        dc_value = d_c.get(self.n_bits, 6)  # Valor padrão de 6 caso não esteja definido

        # Gera as matrizes H e G
        H, G = self.make_ldpc_fixed(self.n_bits, dv_value, dc_value, systematic=True, sparse=True)

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

        # Gerar todas as palavras de informação possíveis (vetores de bits)
        info_words = [list(map(int, format(i, f'0{self.k_bits}b'))) for i in range(size)]

        # Codificar cada palavra de informação para obter a tabela de códigos
        code_table = [self.encode_ldpc(info_word) for info_word in info_words]

        for i in range(len(info_words)):
            print(f'Código: {code_table[i]}')

        return code_table

