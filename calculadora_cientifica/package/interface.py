import customtkinter as ctk
from .calculadora import Calculadora
import os


class App:
    def __init__(self):
        self.calculadora = Calculadora()
        self.historico = self.calculadora.historico
        self.expressao = ""
        self.resultado = ""
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk()
        self.root.title("Calculadora Científica")
        self.root.geometry("360x520")
        self.root.minsize(360, 520) #limitar tamanho mínimo
        self.root.maxsize(360, 520) #limitar tamanho máximo (feita sobre medida)
        self.criar_visor()
        self._atualizar_historico()
        self.criar_teclado()
        self.icone()
        self.cursor_pos = 0  # Posição do cursor
        self.cursor_visible = True  # Estado de visibilidade do cursor
        self.cursor_char = "|"  # Caractere do cursor
        self.blink_speed = 500  # Velocidade do piscar do cursor (ms)
        self.toggle_cursor()
        self.root.mainloop()

    def icone(self):
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "calculadora.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Não foi possível carregar o ícone: {e}")

    def criar_visor(self):
        self.visor_frame = ctk.CTkFrame(self.root, height=120, corner_radius=10)
        self.visor_frame.pack(pady=20, padx=20, fill="x", expand=True)

        self.historico_frame = ctk.CTkFrame(self.visor_frame, width=120)
        self.historico_frame.pack(side="left", fill="y", padx=(0, 10))

        self.historico_label = ctk.CTkLabel(
            self.historico_frame,
            text="Histórico",
            font=("Arial", 12, "bold"))
        self.historico_label.pack(pady=5)

        self.historico_texto = ctk.CTkTextbox(
            self.historico_frame,
            width=120,
            height=100,
            font=("Arial", 10),
            state="disabled")
        self.historico_texto.pack(fill="both", expand=True)

        self.visores_frame = ctk.CTkFrame(self.visor_frame)
        self.visores_frame.pack(side="right", fill="both", expand=True)

        self.visor_superior = ctk.CTkLabel(
            self.visores_frame,
            text="",
            anchor="e",
            font=("Arial", 14),
            height=40)
        self.visor_superior.pack(pady=(0, 5), fill="x")

        self.visor_principal = ctk.CTkLabel(
            self.visores_frame,
            text="0",
            anchor="e",
            font=("Arial", 28, "bold"),
            height=60)
        self.visor_principal.pack(fill="x")

    def toggle_cursor(self):
        """Alterna a visibilidade do cursor (para o efeito piscante)"""
        self.cursor_visible = not self.cursor_visible
        self.atualizar_visor()
        self.root.after(self.blink_speed, self.toggle_cursor)

    def atualizar_visor(self):
        """Atualiza o visor com a expressão atual e o cursor."""
        texto_base = self.expressao  # self.expressao DEVE estar limpa, sem o cursor_char

        texto_para_exibir = texto_base
        if self.cursor_visible:
            texto_para_exibir = (texto_base[:self.cursor_pos] +
                                 self.cursor_char +
                                 texto_base[self.cursor_pos:])

        if not self.expressao and self.cursor_pos == 0:  # Expressão vazia de fato
            # Se cursor visível, mostra só o cursor. Se não, mostra "0"
            self.visor_principal.configure(text=self.cursor_char if self.cursor_visible else "0")
        else:
            self.visor_principal.configure(text=texto_para_exibir)


    def mover_cursor(self, direcao):
        """Move o cursor para esquerda ou direita"""
        self.cursor_pos = max(0, min(len(self.expressao), self.cursor_pos + direcao))
        self.cursor_visible = True  # Torna o cursor visível ao mover
        self.atualizar_visor()

    def criar_teclado(self):
        self.teclado_frame = ctk.CTkFrame(self.root)
        self.teclado_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)

        self.shift_ativado = False

        self.botoes_normal = [
            ['1/2', 'ln', 'log', 'HIS', 'TH'],
            ['sin', 'cos', 'tan', '(', ')'],
            ['7', '8', '9', 'e', 'C'],
            ['4', '5', '6', '*', '/'],
            ['1', '2', '3', '+', '-'],
            ['⌫', '0', ',', '=']
        ]

        self.botoes_shift = [
            ['2/2', 'log₂', '<-', '->', 'TH'],
            ['asin', 'acos', 'atan', '(', ')'],
            ['x²', 'x³', 'x^y', 'π', 'C'],
            ['√', '∛', 'ⁿ√', '*', '/'],
            ['|x|', '!', 'Φ', '+', '-'],
            ['⌫', '0', ',', '='] ]

        self.atualizar_teclado()

    def apagar_ultimo(self):
        """Apaga o caractere antes da posição do cursor."""
        if self.cursor_pos > 0 and self.expressao:  # Só apaga se houver algo antes do cursor
            self.expressao = (self.expressao[:self.cursor_pos - 1] +
                              self.expressao[self.cursor_pos:])
            self.cursor_pos -= 1
            self.atualizar_visor()  # Usa o método centralizado para atualizar o display
        elif not self.expressao:  # Se a expressão já estiver vazia
            self.cursor_pos = 0
            self.atualizar_visor()

    def atualizar_teclado(self):
        for widget in self.teclado_frame.winfo_children():
            widget.destroy()

        layout = self.botoes_shift if self.shift_ativado else self.botoes_normal

        for linha in layout:
            linha_frame = ctk.CTkFrame(self.teclado_frame)
            linha_frame.pack(fill="x", pady=2)

            for texto in linha:
                if texto == '':
                    continue

                btn = ctk.CTkButton(
                    linha_frame,
                    text=texto,
                    width=self.obter_largura_botao(texto),
                    height=45,
                    font=("Arial", 18),
                    command=lambda t=texto: self.botao_pressionado(t))
                btn.pack(side="left", padx=2, pady=2)

                if texto == 'C':
                    btn.configure(fg_color="#d35e60", hover_color="#a83d3f")
                elif texto in ['1/2', '2/2', 'TH']:
                    btn.configure(fg_color="#3498db", hover_color="#2980b9")
                elif texto in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                    btn.configure(fg_color="#9b59b6", hover_color="#8e44ad")

    def obter_largura_botao(self, texto):
        larguras = {
            '0': 124,
            '1/2': 60,
            '2/2': 60,
            'TH': 60,
        }
        return larguras.get(texto, 60)

    def botao_pressionado(self, valor):
        try:
            if valor == 'C':
                self.limpar_tudo()
            elif valor == '=':
                self.calcular()
            elif valor == 'π':
                self.adicionar_expressao('3.141592')
            elif valor == 'e':
                self.adicionar_expressao('2.71828')
            elif valor == 'Φ':
                self.adicionar_expressao('1.618')
            elif valor in ['1/2', '2/2']:
                self.shift()
            elif valor == 'TH':
                self.mudar_tema()
            elif valor == 'HIS':
                self.historico.limpar_historico()
                self._atualizar_historico()
            elif valor in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'ln', 'log', 'log₂']:
                self.adicionar_expressao(f"{valor}(")
            elif valor == '⌫':
                self.apagar_ultimo()
            elif valor in ['x²', 'x³', 'x^y']:
                if valor == 'x²':
                    self.adicionar_expressao('^2')
                elif valor == 'x³':
                    self.adicionar_expressao('^3')
                elif valor == 'x^y':
                    self.adicionar_expressao('^')
            elif valor in ['√', '∛', 'ⁿ√']:
                if valor == '√':
                    self.adicionar_expressao('sqrt(')
                elif valor == '∛':
                    self.adicionar_expressao('^(1/3)')
                elif valor == 'ⁿ√':
                    self.adicionar_expressao('^(1/')
            elif valor == 'log₂':
                self.adicionar_expressao('log₂(')
            elif valor == '|x|':
                self.adicionar_expressao('abs(')
            if valor in ['<-', '->']:
                self.mover_cursor(-1 if valor == '<-' else 1)
            elif valor.isdigit() or valor in ['.', ',']:
                self.adicionar_expressao(valor.replace(',', '.'))
            else:
                self.adicionar_expressao(valor)
        except Exception as e:
            self.mostrar_erro(f"Erro: {str(e)}")

    def adicionar_expressao(self, valor):
        # Primeiro verifica se o valor é algo que NÃO deve ser mostrado na tela
        if valor in ['1/2', 'ln', 'log', 'HIS', 'TH',
                     'sin', 'cos', 'tan','e','C',
                     '⌫','=','2/2', 'log₂', '<-',
                     '->','asin', 'acos', 'atan',
                     'x²', 'x³', 'x^y', 'π','Φ',
                     '√', '∛', 'ⁿ√','|x|']:
            return  # Sai da função sem fazer nada

        # Obtém o texto atual sem o cursor
        texto_atual = self.expressao.replace(self.cursor_char, "")

        # Se estiver vazio ou mostrando "0", reinicia
        if texto_atual in ["", "0"]:
            texto_atual = ""
            self.cursor_pos = 0

        # Insere o novo valor na posição correta
        novo_texto = texto_atual[:self.cursor_pos] + valor + texto_atual[self.cursor_pos:]
        self.expressao = novo_texto
        self.cursor_pos += len(valor)

        # Atualiza o visor (o cursor será posicionado no atualizar_visor)
        self.atualizar_visor()

    def limpar_tudo(self):
        self.expressao = ""
        self.resultado = ""
        self.cursor_pos = 0
        self.visor_superior.configure(text="")
        self.atualizar_visor()

    def calcular(self):
        try:

            if not self.expressao.strip():  # Não calcular se expressão estiver vazia
                return

            resultado = self.calculadora.avaliar_expressao(self.expressao)

            if isinstance(resultado, str) and resultado.startswith("Erro"):
                raise ValueError(resultado)

            self.historico.adicionar_operacao(self.expressao, resultado)
            self._atualizar_historico()

            self.visor_superior.configure(text=self.expressao)


            if isinstance(resultado, float):
                if resultado == 0.0:  # <-- Checagem explícita para 0.0
                    resultado_formatado = "0"
                elif abs(resultado) > 1e9 or (abs(resultado) < 1e-6 and resultado != 0.0): # Usei 1e9 para números grandes, e 1e-6 para pequenos não-zero
                    resultado_formatado = f"{resultado:.6e}" # Notação científica para números muito grandes ou muito pequenos (mas não zero)
                else:
                    # Formatação padrão para outros números float
                    # Usar uma boa quantidade de casas decimais para precisão interna antes de cortar os zeros
                    temp_str = f"{resultado:.8f}"  # Ex: 8 casas decimais
                    temp_str = temp_str.rstrip('0') # Remove zeros à direita (ex: "5.1200" -> "5.12")
                    if temp_str.endswith('.'):      # Se terminar com um ponto (ex: "5.")
                        temp_str = temp_str.rstrip('.') # Remove o ponto (ex: "5." -> "5")
                    resultado_formatado = temp_str if temp_str else "0" # Garante que não fique vazio (ex: se o resultado fosse 0.00000000001 e .8f o tornasse "0")

            else: # Se não for float (ex: se alguma operação retornar um int diretamente)
                resultado_formatado = str(resultado)

            # Atualiza o visor principal com o resultado formatado
            self.visor_principal.configure(text=resultado_formatado)
            self.expressao = resultado_formatado
            self.cursor_pos = len(self.expressao)

        except ValueError as e:
            self.mostrar_erro(str(e))
        except ZeroDivisionError:
            self.mostrar_erro("Divisão por zero")
        except Exception as e:
            self.mostrar_erro(f"Erro inesperado: {str(e)}")

    def mostrar_erro(self, mensagem):
        self.visor_principal.configure(text=mensagem, text_color="red")
        self.root.after(2000, self.limpar_erro)

    def limpar_erro(self):
        self.visor_principal.configure(text_color="white")
        self.limpar_tudo()

    def shift(self):
        self.shift_ativado = not self.shift_ativado
        self.atualizar_teclado()

    def mudar_tema(self):
        tema_atual = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if tema_atual == "Dark" else "Dark")

    def _atualizar_historico(self):
        self.historico_texto.configure(state="normal")
        self.historico_texto.delete("1.0", "end")

        for operacao in self.historico.obter_historico():
            self.historico_texto.insert("end", f"{operacao[0]} = {operacao[1]}\n")

        self.historico_texto.configure(state="disabled")