# Calculadora Científica em Python com CustomTkinter

## ✒️ Definição do Problema

O objetivo deste projeto é desenvolver uma calculadora científica funcional utilizando a linguagem Python e o paradigma de Programação Orientada a Objetos. A calculadora deve possuir uma interface gráfica intuitiva construída com a biblioteca CustomTkinter, permitir a realização de operações matemáticas básicas e científicas, e manter um histórico persistente dos cálculos realizados.

## ✨ Funcionalidades Principais

A calculadora oferece as seguintes funcionalidades:

* **Operações Básicas:** Adição (`+`), Subtração (`-`), Multiplicação (`*`), Divisão (`/`).
* **Operações Científicas (Modo Normal e Shift):**
    * Logaritmos: Natural (`ln`), base 10 (`log`), base 2 (`log₂`).
    * Trigonométricas: Seno (`sin`), Cosseno (`cos`), Tangente (`tan`).
    * Trigonométricas Inversas: Arco seno (`asin`), Arco cosseno (`acos`), Arco tangente (`atan`).
    * Potenciação: Quadrado (`x²`), Cubo (`x³`), Elevado a y (`x^y`).
    * Raízes: Raiz quadrada (`√`), Raiz cúbica (`∛`), Raiz n-ésima (`ⁿ√`).
    * Outras: Fatorial (`!`), Valor absoluto (`|x|`), Inserção de parênteses (`(`, `)`).
* **Constantes:**
    * Pi (`π`): 3.141592...
    * Número de Euler (`e`): 2.71828...
    * Número de Ouro (`Φ`): 1.618...
* **Gerenciamento de Expressão:**
    * Entrada de expressões com múltiplos operadores e funções.
    * Limpar entrada atual (`C`).
    * Apagar último caractere/elemento (`⌫`).
    * Navegação na expressão com cursor (`<-`, `->`).
* **Histórico de Cálculos:**
    * Visualização das últimas operações realizadas.
    * Opção para limpar todo o histórico (`HIS`).
    * Persistência do histórico em um banco de dados SQLite (`historico_calc.db`).
* **Interface Gráfica:**
    * Tema claro e escuro, com botão de alternância (`TH`).
    * Layout responsivo e botões organizados para fácil utilização.
    * Visor principal para a expressão atual e visor superior para a última expressão calculada.
    * Teclado com dois modos de operação (normal e shift `1/2`, `2/2`).

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.13
* **Paradigma de Programação:** Orientação a Objetos
* **Interface Gráfica (GUI):** CustomTkinter
* **Banco de Dados (Histórico):** SQLite3 (módulo nativo do Python)
* **Módulos Python Adicionais:** `os`, `math`, `datetime`, `pickle` (para serialização opcional)

## 📂 Estrutura do Projeto

O projeto está organizado da seguinte forma:

* `main.py`: Arquivo principal que inicializa e executa a aplicação da calculadora.
* `README.md`: Este arquivo, contendo a documentação do projeto.
* `package/`: Pasta (pacote Python) contendo os módulos principais do sistema:
    * `__init__.py`: Inicializador do pacote.
    * `calculadora.py`: Define a classe `Calculadora`, o motor de cálculo que processa as expressões.
    * `interface.py`: Define a classe `App`, responsável por construir e gerenciar toda a interface gráfica e interações do usuário.
    * `historico.py`: Define a classe `Historico`, que gerencia o armazenamento e recuperação do histórico de cálculos usando SQLite.
    * `operacoes.py`: Define as classes `OperacaoBase`, `OperacoesBasicas` e `OperacoesCientificas`, contendo a lógica para cada operação matemática.
    * `mixins.py`: Contém classes Mixin, como `RoundMixin` para funcionalidades de arredondamento.
    * `calculadora.ico`: Ícone da aplicação.

## 💡 Princípios de Orientação a Objetos Aplicados

Este projeto foi desenvolvido seguindo o paradigma de Orientação a Objetos, aplicando os seguintes conceitos:

* **Encapsulamento:** Cada classe (`Calculadora`, `Historico`, `App`, `OperacoesBasicas`, etc.) agrupa seus dados (atributos) e os comportamentos (métodos) que os manipulam. Atributos são frequentemente protegidos (convenção `_privado`) e acessados via métodos ou propriedades.
* **Herança:**
    * A classe `Calculadora` herda de `OperacoesBasicas` e `OperacoesCientificas`, reutilizando os métodos de cálculo.
    * As classes `OperacoesBasicas` e `OperacoesCientificas` herdam de uma classe `OperacaoBase` (para validação de entrada) e também do `RoundMixin`.
* **Polimorfismo:**
    * O método `_round()` do `RoundMixin` é utilizado polimorficamente pelas diferentes classes de operações.
    * A forma como `avaliar_expressao` na `Calculadora` pode chamar diferentes funções matemáticas (herdadas) com base na entrada também demonstra polimorfismo.
* **Abstração:** As classes fornecem interfaces simplificadas para funcionalidades complexas. Por exemplo, a classe `App` interage com a `Calculadora` através de métodos como `avaliar_expressao` sem precisar conhecer os detalhes internos de como cada operação é calculada.
* **Composição (Forte):**
    * A classe `Calculadora` possui uma instância da classe `Historico` (`self._historico = Historico()`). O ciclo de vida do objeto `Historico` está ligado ao da `Calculadora` neste contexto.
* **Associação (Fraca):**
    * A classe `App` (interface) cria e utiliza uma instância da `Calculadora` (`self.calculadora = Calculadora()`). A `App` "usa um" `Calculadora`.
* **Mixins:**
    * A classe `RoundMixin` é utilizada para adicionar a funcionalidade de arredondamento de forma modular às classes de operações (`OperacoesBasicas` e `OperacoesCientificas`) sem a necessidade de uma herança mais rígida.

## 📋 Casos de Uso

A seguir, são apresentados os principais casos de uso do sistema:

### CU-01: Realizar Cálculo Básico
* **Ator:** Usuário
* **Pré-condições:** Calculadora aberta.
* **Fluxo Principal:**
    1.  Usuário insere o primeiro número usando os botões numéricos.
    2.  Usuário pressiona um botão de operação básica (ex: `+`, `-`, `*`, `/`).
    3.  Usuário insere o segundo número.
    4.  Usuário pressiona o botão `=`.
    5.  O sistema exibe o resultado no visor principal.
    6.  O sistema armazena a expressão e o resultado no histórico.
* **Fluxo Alternativo (Erro na Expressão):**
    1.  Se a expressão for inválida (ex: divisão por zero, sintaxe incorreta).
    2.  O sistema exibe uma mensagem de erro no visor principal.
    3.  O usuário pode corrigir a expressão usando `C` ou `⌫` e tentar novamente.

### CU-02: Utilizar Função Científica
* **Ator:** Usuário
* **Pré-condições:** Calculadora aberta.
* **Fluxo Principal (Exemplo com `sin`):**
    1.  Usuário pressiona o botão da função desejada (ex: `sin`). O visor exibe "sin(".
    2.  Usuário insere o valor do ângulo (ex: "90").
    3.  Usuário pressiona o botão `)`. O visor exibe "sin(90)".
    4.  Usuário pressiona o botão `=`.
    5.  O sistema exibe o resultado (ex: "1") no visor principal.
    6.  O sistema armazena a expressão e o resultado no histórico.
* **Fluxo Alternativo (Entrada Inválida para Função):**
    1.  Se o valor fornecido para a função estiver fora do domínio válido (ex: `asin(2)`).
    2.  O sistema exibe uma mensagem de erro específica.

### CU-03: Consultar Histórico de Cálculos
* **Ator:** Usuário
* **Pré-condições:** Pelo menos um cálculo foi realizado e armazenado.
* **Fluxo Principal:**
    1.  O usuário visualiza o painel de histórico na interface.
    2.  O sistema exibe as últimas operações realizadas (expressão = resultado).

### CU-04: Limpar Histórico de Cálculos
* **Ator:** Usuário
* **Pré-condições:** Calculadora aberta.
* **Fluxo Principal:**
    1.  Usuário pressiona o botão `HIS`.
    2.  O sistema remove todos os registros do histórico de cálculos (do banco de dados).
    3.  O sistema atualiza a exibição do painel de histórico, que agora estará vazio.

### CU-05: Utilizar Funções com Tecla Shift
* **Ator:** Usuário
* **Pré-condições:** Calculadora aberta.
* **Fluxo Principal (Exemplo com `x²`):**
    1.  Usuário pressiona o botão `1/2` (ou `2/2` para reverter) para ativar/desativar o modo Shift. Os rótulos dos botões mudam.
    2.  Usuário insere um número (ex: "5").
    3.  Usuário pressiona o botão da função desejada no modo Shift (ex: `x²`). O visor adiciona "^2".
    4.  Usuário pressiona o botão `=`.
    5.  O sistema exibe o resultado (ex: "25") no visor principal.
    6.  O sistema armazena a expressão e o resultado no histórico.

### CU-06: Mudar Tema da Interface
* **Ator:** Usuário
* **Pré-condições:** Calculadora aberta.
* **Fluxo Principal:**
    1.  Usuário pressiona o botão `TH`.
    2.  O sistema alterna o tema da interface entre Claro (Light) e Escuro (Dark).

### CU-07: Inserir Constantes
* **Ator:** Usuário
* **Pré-condições:** Calculadora aberta.
* **Fluxo Principal (Exemplo com `π`):**
    1.  Usuário (se necessário) ativa o modo Shift para acessar `π`.
    2.  Usuário pressiona o botão `π`.
    3.  A calculadora insere o valor numérico de Pi (ex: "3.141592") na expressão atual.

### CU-08: Editar Expressão
* **Ator:** Usuário
* **Pré-condições:** Uma expressão está sendo digitada no visor.
* **Fluxo Principal (Apagar):**
    1.  Usuário pressiona o botão `⌫`.
    2.  O sistema apaga o caractere à esquerda da posição atual do cursor.
    3.  O cursor é reposicionado.
* **Fluxo Principal (Navegar com Cursor):**
    1.  Usuário (se necessário) ativa o modo Shift para acessar `<-` ou `->`.
    2.  Usuário pressiona `<-` ou `->`.
    3.  O cursor se move para a esquerda ou direita na expressão atual, permitindo inserção ou deleção em pontos específicos.

## ⚙️ Como Operar / Instruções de Uso

1.  **Entrada de Números e Operadores Básicos:**
    * Clique nos botões numéricos (`0`-`9`) e no separador decimal (`,`) para formar números.
    * Clique nos botões de operação (`+`, `-`, `*`, `/`) entre os números.
    * Pressione `=` para calcular o resultado.

2.  **Funções Comuns (com parênteses automáticos):**
    * Para funções como `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `log`, `ln`, `log₂`, `sqrt` (raiz quadrada) e `abs` (valor absoluto):
        * Pressione o botão da função. Ela será inserida com um parêntese de abertura (ex: `sin(`, `sqrt(`, `abs(`).
        * Digite o argumento da função.
        * Feche o parêntese `)` se necessário (especialmente se houver mais partes na expressão).
        * Pressione `=` para calcular.
    * **Exemplo `abs(` para `|x|`:** Ao pressionar o botão `|x|`, a calculadora insere `abs(`. Complete com o número e feche o parêntese: `abs(-5)`.

3.  **Potenciação e Raízes (Entrada Manual da Sintaxe):**
    * **Quadrado (`x²`):** Após inserir um número (ex: `5`), pressione `x²`. A calculadora adicionará `^2` à sua expressão (ex: `5^2`).
    * **Cubo (`x³`):** Após inserir um número (ex: `4`), pressione `x³`. A calculadora adicionará `^3` à sua expressão (ex: `4^3`).
    * **Elevado a y (`x^y`):** Insira a base (ex: `2`), pressione `x^y` (que insere `^`), e então insira o expoente (ex: `10`). A expressão ficará `2^10`.
    * **Raiz Cúbica (`∛`):** Após inserir o radicando (ex: `27`), pressione `∛`. A calculadora adicionará `^(1/3)` à sua expressão (ex: `27^(1/3)`).
    * **Raiz n-ésima (`ⁿ√`):** Após inserir o radicando (ex: `16`), pressione `ⁿ√`. A calculadora adicionará `^(1/` à sua expressão. Você precisará completar o índice da raiz e fechar o parêntese (ex: `16^(1/4)` para raiz quarta). **Atenção:** Complete a expressão corretamente (ex: `numero^(1/indice)`).

4.  **Tecla Shift (`1/2` e `2/2`):**
    * Pressione `1/2` para acessar o segundo conjunto de funções nos botões (ex: `x²`, `√`, `asin`, etc.). O rótulo do botão mudará para `2/2`.
    * Pressione `2/2` para retornar ao conjunto de funções normal.

5.  **Edição da Expressão:**
    * `C`: Limpa toda a expressão atual no visor principal.
    * `⌫`: Apaga o caractere ou função imediatamente à esquerda do cursor.
    * `<-` / `->` (geralmente no modo Shift): Movem o cursor dentro da expressão para edição.

6.  **Histórico:**
    * O painel lateral exibe as últimas operações.
    * `HIS`: Limpa todo o histórico de cálculos.

7.  **Tema:**
    * `TH`: Alterna entre o tema claro e escuro da interface.

8.  **Constantes (`π`, `e`, `Φ`):**
    * Pressione o botão correspondente (pode estar no modo normal ou Shift). O valor da constante será inserido na expressão.
## 🚀 Como Executar o Projeto

1.  **Pré-requisitos:**
    * Python 3.8 ou superior instalado.
    * `pip` (gerenciador de pacotes Python) instalado.

2.  **Instalação de Dependências:**
    * Abra um terminal ou prompt de comando.
    * Navegue até a pasta raiz do projeto.
    * Instale a biblioteca CustomTkinter:
        ```bash
        pip install customtkinter
        ```

3.  **Executando a Calculadora:**
    * Ainda no terminal, na pasta raiz do projeto, execute o `main.py`:
        ```bash
        python main.py
        ```
    * A interface gráfica da calculadora deverá aparecer.

## 👤 Autor

* Davi Severiano - Estudante de Engenharia de Software

---