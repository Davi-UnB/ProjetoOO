class RoundMixin:
    """
    Mixin que fornece um método para arredondar valores numericos.
    Útil para padronizar a precisão dos resultados das operações.
    """
    def _round(self, value, casas_decimais=6):
        """
        Arredonda um valor para um número especificado de casas decimais.

        Args:
            value: O valor a ser arredondado (espera-se int ou float).
            casas_decimais (int): O número de casas decimais para o arredondamento.

        Returns:
            float | Any: O valor arredondado, ou o valor original se não for numérico.
        """
        if isinstance(value, (int, float)):
            return round(value, casas_decimais)
        return value