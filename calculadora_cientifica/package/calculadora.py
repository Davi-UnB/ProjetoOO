from .operacoes import OperacoesBasicas, OperacoesCientificas
from .historico import Historico
# Import math para ter acesso a constantes como pi e e, se necessário diretamente aqui.
# No entanto, as operações já usam math.
import math


class Calculadora(OperacoesBasicas, OperacoesCientificas):
    """
    Classe principal da calculadora científica.

    Combina operações básicas e científicas, gerencia histórico de cálculos
    e fornece interface para avaliação de expressões matemáticas.

    Attributes:
        _historico (Historico): Instância para armazenamento do histórico de operações.
                                Esta é uma composição forte.
        answer (float | None): Último resultado calculado, None se nenhum cálculo foi feito.
    """

    def __init__(self):
        """Inicializa a calculadora, criando uma instância de Historico."""
        super().__init__()  # Importante chamar __init__ das classes base se elas tiverem (compatibilidade futura)
        self._historico = Historico()  # Composição forte
        self.answer = None

    def avaliar_expressao(self, expr: str):
        """
        Avalia uma expressão matemática fornecida como string.

        Realiza substituições para compatibilidade com a função eval e
        processa operações especiais como fatorial antes da avaliação principal.

        Args:
            expr (str): A expressão matemática a ser avaliada.

        Returns:
            float | str: O resultado da avaliação ou uma mensagem de erro.
        """
        try:
            # Padroniza a expressão para avaliação
            # Substitui vírgula por ponto para números decimais
            # Substitui ^ por ** para exponenciação
            # Substitui log₂ por log2 (função interna)
            # Remove espaços extras para evitar problemas com eval
            expr_eval = expr.replace(',', '.').replace('^', '**').replace('log₂', 'log2').strip()

            # Se a expressão for apenas um número, retorna-o diretamente
            # (após arredondamento)
            if expr_eval.replace('.', '', 1).isdigit() or \
                    (expr_eval.startswith('-') and expr_eval[1:].replace('.', '', 1).isdigit()):
                return self._round(float(expr_eval))

            # Processa fatoriais antes da avaliação principal
            # Esta lógica de fatorial funciona para números simples antes do '!'
            # Ex: "5!", "10!*2". Para expressões como "(2+1)!", o usuário
            # precisaria calcular "2+1" primeiro.
            while '!' in expr_eval:
                idx = expr_eval.index('!')
                if idx == 0:
                    raise ValueError("Sintaxe inválida para fatorial: '!' no início.")

                num_str = ''
                i = idx - 1
                # Extrai o número imediatamente antes do '!'
                # Permite números decimais, mas fatorial só se aplica a inteiros
                while i >= 0 and (expr_eval[i].isdigit() or expr_eval[i] == '.'):
                    num_str = expr_eval[i] + num_str
                    i -= 1

                if not num_str:
                    raise ValueError("Sintaxe inválida para fatorial: Nenhum número antes do '!'.")

                num_val = float(num_str)
                if not num_val.is_integer():
                    raise ValueError("Fatorial é definido apenas para números inteiros.")

                # Calcula o fatorial usando o método da classe OperacoesCientificas
                fat_result = self.fatorial(int(num_val))
                expr_eval = expr_eval[:i + 1] + str(fat_result) + expr_eval[idx + 1:]

                # Se após a substituição do fatorial a expressão se tornou um número simples
                if expr_eval.replace('.', '', 1).isdigit() or \
                        (expr_eval.startswith('-') and expr_eval[1:].replace('.', '', 1).isdigit()):
                    return self._round(float(expr_eval))

            # Define o escopo para a função eval
            # Permite apenas funções matemáticas seguras e os métodos da calculadora
            # math_functions é um dicionário que mapeia nomes de string (usados na expressão)
            # para os métodos correspondentes da calculadora.
            math_functions = {
                'sin': self.seno_graus,
                'cos': self.cosseno_graus,
                'tan': self.tangente_graus,
                'asin': self.arcoseno_graus,
                'acos': self.arcocosseno_graus,
                'atan': self.arcotangente_graus,
                'log': self.log10,  # log na calculadora geralmente é base 10
                'ln': self.log_natural,
                'sqrt': self.raiz_quadrada,
                'log2': self.log2,  # log na base 2
                'abs': self.modulo,  # valor absoluto
                # Adicionar outras funções/constantes aqui se necessário
            }

            # Avalia a expressão.
            # '__builtins__': None restringe o acesso a funções built-in perigosas.
            # math_functions fornece as funções seguras.
            resultado = eval(expr_eval, {'__builtins__': None}, math_functions)

            self.answer = self._round(resultado)  # Arredonda e armazena o último resultado
            return self.answer
        except ZeroDivisionError:
            return "Erro: Divisão por zero"
        except ValueError as ve:  # Erros de valor (ex: log de num negativo)
            return f"Erro: {ve}"
        except TypeError as te:  # Erros de tipo (ex: sin())
            return f"Erro de tipo: {te}"
        except SyntaxError:
            return "Erro de sintaxe na expressão"
        except Exception as e:
            # Captura outras exceções inesperadas
            return f"Erro inesperado: {e}"

    @property
    def historico(self):
        """Propriedade para acessar o histórico de cálculos."""
        return self._historico