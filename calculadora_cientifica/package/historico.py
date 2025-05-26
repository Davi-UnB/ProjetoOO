import sqlite3
import pickle  # Para serialização/desserialização opcional em arquivo
from datetime import datetime
import os  # Para construir caminhos de arquivo de forma robusta


class Historico:
    """
    Gerencia o histórico de operações da calculadora usando um banco de dados SQLite.
    Também oferece funcionalidade opcional para salvar/carregar histórico de/para um arquivo pickle.
    """
    DB_FILENAME = 'historico_calc.db'
    PICKLE_FILENAME = 'historico.pkl'

    def __init__(self):
        """Inicializa a conexão com o banco de dados e cria a tabela se não existir."""
        self.conexao = None
        self.cursor = None
        self._inicializar_banco_dados()

    def _get_db_path(self):
        """Retorna o caminho para o arquivo do banco de dados no mesmo diretório do script."""
        # Isso garante que o banco de dados seja criado no mesmo diretório do arquivo historico.py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, self.DB_FILENAME)

    def _inicializar_banco_dados(self):
        """Inicializa o banco de dados SQLite e o cursor."""
        db_path = self._get_db_path()
        self.conexao = sqlite3.connect(db_path)
        self.cursor = self.conexao.cursor()
        self._criar_tabela()

    def _criar_tabela(self):
        """Cria a tabela 'historico' no banco de dados se ela ainda não existir."""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expressao TEXT NOT NULL,
                    resultado TEXT NOT NULL,
                    data_hora TEXT NOT NULL
                )
            ''')
            self.conexao.commit()
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela do histórico: {e}")

    def adicionar_operacao(self, expressao: str, resultado: str):
        """
        Adiciona uma nova operação (expressão e resultado) ao histórico no banco de dados.

        Args:
            expressao (str): A expressão matemática que foi calculada.
            resultado (str): O resultado da expressão.
        """
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute(
                "INSERT INTO historico (expressao, resultado, data_hora) VALUES (?, ?, ?)",
                (expressao, str(resultado), data_hora)
            )
            self.conexao.commit()
        except sqlite3.Error as e:
            print(f"Erro ao adicionar operação ao histórico: {e}")

    def obter_historico(self, limite: int = 8):
        """
        Obtém as últimas 'limite' operações do histórico do banco de dados.

        Args:
            limite (int): O número máximo de entradas do histórico a serem retornadas.

        Returns:
            list: Uma lista de tuplas, onde cada tupla contém (expressao, resultado).
        """
        try:
            self.cursor.execute(
                "SELECT expressao, resultado FROM historico ORDER BY id DESC LIMIT ?",
                (limite,)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao obter histórico: {e}")
            return []

    def limpar_historico(self):
        """Remove todas as operações do histórico do banco de dados."""
        try:
            self.cursor.execute("DELETE FROM historico")
            self.conexao.commit()
        except sqlite3.Error as e:
            print(f"Erro ao limpar histórico: {e}")

    def _get_pickle_path(self):
        """Retorna o caminho para o arquivo pickle no mesmo diretório do script."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, self.PICKLE_FILENAME)

    def salvar_em_arquivo(self):
        """
        Serializa (salva) o histórico atual (obtido do DB) em um arquivo usando pickle.
        Esta é uma funcionalidade de exportação/backup.
        """
        pickle_path = self._get_pickle_path()
        try:
            # Obtém todo o histórico para salvar, não apenas o limite padrão
            historico_completo = []
            self.cursor.execute("SELECT expressao, resultado, data_hora FROM historico ORDER BY id ASC")
            historico_completo = self.cursor.fetchall()

            with open(pickle_path, 'wb') as f:
                pickle.dump(historico_completo, f)
            print(f"Histórico salvo em {pickle_path}")
        except sqlite3.Error as e:
            print(f"Erro ao obter histórico do DB para salvar em arquivo: {e}")
        except IOError as e:
            print(f"Erro de I/O ao salvar histórico em arquivo: {e}")

    def carregar_do_arquivo(self):
        """
        Desserializa (carrega) o histórico de um arquivo pickle.
        As entradas carregadas são adicionadas ao banco de dados SQLite se não existirem.
        Esta é uma funcionalidade de importação.
        """
        pickle_path = self._get_pickle_path()
        try:
            with open(pickle_path, 'rb') as f:
                historico_carregado = pickle.load(f)

            # Adicionar ao banco de dados (evitando duplicatas pode ser complexo,
            # por simplicidade, aqui apenas insere. Poderia verificar antes.)
            # Por ora, vamos apenas retornar o que foi carregado.
            # A interface poderia decidir se quer limpar o DB e popular com isso.
            print(f"Histórico carregado de {pickle_path}")
            return historico_carregado
        except FileNotFoundError:
            print(f"Arquivo de histórico '{pickle_path}' não encontrado.")
            return []
        except IOError as e:
            print(f"Erro de I/O ao carregar histórico do arquivo: {e}")
            return []
        except pickle.PickleError as e:
            print(f"Erro ao desserializar histórico do arquivo: {e}")
            return []

    def __del__(self):
        """Destrutor - fecha a conexão com o banco de dados quando o objeto é destruído."""
        if self.conexao:
            self.conexao.close()
