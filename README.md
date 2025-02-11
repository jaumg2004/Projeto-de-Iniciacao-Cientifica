# Estabelicimento de chave criptografica utilizando o ganho do canal sem fio como segredo - parte 2

Este projeto realiza a simulação de diferentes cenários de transmissão de dados em canais ruidosos, utilizando códigos corretores de erro como Hamming, BCH, LDPC e Golay. A simulação envolve a geração de sequências de bits, sua transmissão por canais de comunicação com diferentes níveis de ruído e a análise do desempenho dos códigos corretores de erro.

📌 Estrutura do Código

CodeGenerator: Classe responsável pela geração das tabelas de código.

Cenário1 - Cenário5: Classes que modelam diferentes cenários de ruído.

Plotagem: Classe que gerencia a visualização gráfica dos resultados.

main.py: Script principal que executa a simulação.

🚀 Como Usar

1️⃣ Instalação

Certifique-se de ter o Python instalado e instale as dependências necessárias:

pip install numpy matplotlib

2️⃣ Execução

Execute o script principal com:

python main.py

3️⃣ Entradas do Usuário

Durante a execução, o usuário deve fornecer as seguintes informações:

Método de reconciliação: Escolha entre 1 ou 2.

Quantidade de testes: Número de simulações a serem realizadas.

Código corretor de erro: Escolha entre Hamming, BCH, LDPC ou Golay.

Tamanho da cadeia de bits: Para códigos diferentes de Golay, escolha entre 7, 15, 127, 255.

Plotagem de resultados: Opção de visualizar gráficos (y para sim, n para não).

4️⃣ Saída

O código exibe as porcentagens de acerto nos diferentes cenários de ruído e gera gráficos representando os resultados da simulação.

🔧 Estrutura dos Canais

Os seguintes canais são simulados:

Ruído Nulo Canal Unitário

Baixo Ruído Canal Unitário

Baixo Ruído Canal Rayleigh

Alto Ruído Canal Unitário

Alto Ruído Canal Rayleigh

Cada um desses canais afeta a transmissão dos bits e influencia a taxa de erro na recuperação da informação.

⏳ Tempo de Execução

O código mede o tempo total de execução e exibe o tempo decorrido ao final da simulação.

📊 Visualização de Dados

Os resultados são apresentados graficamente usando a classe Plotagem, com diferentes métodos de visualização para o código Golay e os demais códigos corretores de erro.

Este projeto faz parte de uma iniciativa de pesquisa sobre segurança em canais sem fio e técnicas de correção de erros. Para mais informações ou colaborações, entre em contato!
