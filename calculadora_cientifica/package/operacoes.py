import math
from .mixins import RoundMixin  # Importa o mixin de arredondamento


class OperacaoBase:
    """
    Classe base para operações, fornecendo validação de entrada.
    Não herda de RoundMixin diretamente, pois as subclasses decidirão se usam.
    """

    def validar_entrada(self, *args):
        """
        Valida se todas as entradas podem ser convertidas para float.

        Args:
            *args: Um número variável de argumentos a serem validados.

        Returns:
            list[float]: Uma lista dos argumentos convertidos para float.

        Raises:
            ValueError: Se algum argumento não puder ser convertido para float.
        """
        try:
            return [float(arg) for arg in args]
        except ValueError:
            raise ValueError("Entrada inválida.")


class OperacoesBasicas(OperacaoBase, RoundMixin):  # Herda de OperacaoBase e RoundMixin
    """Define operações matemáticas básicas."""

    def soma(self, a, b):
        a, b = self.validar_entrada(a, b)
        return self._round(a + b)

    def subtracao(self, a, b):
        a, b = self.validar_entrada(a, b)
        return self._round(a - b)

    def multiplicacao(self, a, b):
        a, b = self.validar_entrada(a, b)
        return self._round(a * b)

    def divisao(self, a, b):
        a, b = self.validar_entrada(a, b)
        if b == 0:
            raise ZeroDivisionError("Divisão por zero não permitida.")
        return self._round(a / b)


class OperacoesCientificas(OperacaoBase, RoundMixin):  # Herda de OperacaoBase e RoundMixin
    """Define operações matemáticas científicas."""

    def seno_graus(self, angulo_graus):
        """Calcula o seno de um ângulo em graus."""
        angulo_graus = self.validar_entrada(angulo_graus)[0]
        return self._round(math.sin(math.radians(angulo_graus)))

    def cosseno_graus(self, angulo_graus):
        """Calcula o cosseno de um ângulo em graus."""
        angulo_graus = self.validar_entrada(angulo_graus)[0]
        return self._round(math.cos(math.radians(angulo_graus)))

    def tangente_graus(self, angulo_graus):
        """Calcula a tangente de um ângulo em graus."""
        angulo_graus = self.validar_entrada(angulo_graus)[0]
        # Verifica ângulos onde a tangente é indefinida (90, 270, etc.)
        if math.isclose(math.cos(math.radians(angulo_graus)), 0.0):
            raise ValueError("Tangente indefinida para este ângulo (divisão por zero).")
        return self._round(math.tan(math.radians(angulo_graus)))

    def arcoseno_graus(self, valor):
        """Calcula o arco seno (em graus) de um valor."""
        valor = self.validar_entrada(valor)[0]
        if not (-1 <= valor <= 1):
            raise ValueError("Entrada para arcoseno deve estar entre -1 e 1.")
        return self._round(math.degrees(math.asin(valor)))

    def arcocosseno_graus(self, valor):
        """Calcula o arco cosseno (em graus) de um valor."""
        valor = self.validar_entrada(valor)[0]
        if not (-1 <= valor <= 1):
            raise ValueError("Entrada para arcocosseno deve estar entre -1 e 1.")
        return self._round(math.degrees(math.acos(valor)))

    def arcotangente_graus(self, valor):
        """Calcula o arco tangente (em graus) de um valor."""
        valor = self.validar_entrada(valor)[0]
        return self._round(math.degrees(math.atan(valor)))

    def log_natural(self, valor):  # ln
        """Calcula o logaritmo natural (base e)."""
        valor = self.validar_entrada(valor)[0]
        if valor <= 0:
            raise ValueError("Logaritmo natural requer entrada positiva.")
        return self._round(math.log(valor))

    def log10(self, valor):  # log (base 10)
        """Calcula o logaritmo na base 10."""
        valor = self.validar_entrada(valor)[0]
        if valor <= 0:
            raise ValueError("Logaritmo base 10 requer entrada positiva.")
        return self._round(math.log10(valor))

    def raiz_quadrada(self, valor):  # sqrt
        """Calcula a raiz quadrada."""
        valor = self.validar_entrada(valor)[0]
        if valor < 0:
            raise ValueError("Raiz quadrada de número negativo não é real.")
        return self._round(math.sqrt(valor))

    def log2(self, valor):  # log base 2
        """Calcula o logaritmo na base 2."""
        valor = self.validar_entrada(valor)[0]
        if valor <= 0:
            raise ValueError("Logaritmo base 2 requer entrada positiva.")
        return self._round(math.log2(valor))

    def modulo(self, valor):  # abs (valor absoluto)
        """Calcula o valor absoluto (módulo) de um número."""
        valor = self.validar_entrada(valor)[0]
        return self._round(abs(valor))

    def fatorial(self, valor):
        """Calcula o fatorial de um número inteiro não negativo."""
        # A validação de entrada já converte para float.
        # Precisamos garantir que seja um inteiro.
        num_float = self.validar_entrada(valor)[0]
        if not num_float.is_integer() or num_float < 0:
            raise ValueError("Fatorial é definido apenas para inteiros não negativos.")
        try:
            return self._round(math.factorial(int(num_float)))
        except OverflowError:
            raise ValueError("Resultado do fatorial muito grande para calcular.")
