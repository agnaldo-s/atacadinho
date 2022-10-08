import sqlite3
import database
from abc import abstractmethod, ABC

class BancoDeDados:
    @staticmethod
    def criar(self):
        conn = sqlite3.connect('/home/agnaldo/Documentos/jovemProgramador/ProjetoIntegrador/project/atacadinho.db')
        conn.execute('PRAGMA foreign_keys=on')
        conn_cursor = conn.cursor()
        ddl = """
            CREATE TABLE IF NOT EXISTS pessoas(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                nome VARCHAR(70) NOT NULL,
                cpf VARCHAR(11) NOT NULL UNIQUE,
                dt_nasc DATE NOT NULL,
                telefone VARCHAR(13) NOT NULL,
                email VARCHAR(60) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tiposFuncionarios(
                id_tipoFunc INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                descricao VARCHAR(70) NOT NULL                        
            );

            CREATE TABLE IF NOT EXISTS funcionarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                dt_cadastro DATE NOT NULL,
                pessoa_id INTEGER NOT NULL,
                tipoFunc_id INTERGER NOT NULL,
                CONSTRAINT fk_funcionario_tipoFuncionarios
                    FOREIGN KEY(tipoFunc_id)
                    REFERENCES tiposFuncionarios(id_tipoFunc)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                CONSTRAINT fk_funcionario_pessoa
                    FOREIGN KEY(pessoa_id)
                    REFERENCES pessoas(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS logins(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                nome_usuario VARCHAR(60) NOT NULL,
                senha VARCHAR(60) NOT NULL,
                funcionario_id INTEGER NULL,
                CONSTRAINT fk_login_funcionario
                    FOREIGN KEY(funcionario_id)
                    REFERENCES funcionarios(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS categorias(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                descricao VARCHAR(255) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS produtos(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                nome VARCHAR(60) NOT NULL,
                valor_unitario DECIMAL(10,2),
                funcionarios_id INTEGER NOT NULL,
                categoria_id INTEGER NOT NULL,
                CONSTRAINT fk_produtos_funcionarios
                    FOREIGN KEY(funcionarios_id)
                    REFERENCES funcionarios(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                CONSTRAINT fk_produtos_categorias
                    FOREIGN KEY(categoria_id)
                    REFERENCES categorias(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
        
            CREATE TABLE IF NOT EXISTS registro_movimentacao(
                id_registro_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS estoque(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                id_registro_movimentacao INTEGER NOT NULL,
                data_hora DATETIME default current_timestamp,
                id_funcionario INTERGER NOT NULL,
                CONSTRAINT fk_estoque_registro_movimentacao
                    FOREIGN KEY(id_registro_movimentacao)
                    REFERENCES registro_movimentacao(id_registro_movimentacao)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                CONSTRAINT fk_estoque_funcionarios
                    FOREIGN KEY(id_funcionario)
                    REFERENCES funcionarios(id)
                CONSTRAINT fk_estoque_produtos
                    FOREIGN KEY(produto_id)
                    REFERENCES produtos(id)
            );
        """

        with conn:
            conn_cursor.executescript(ddl)


    def validar_login(conn, conn_cursor, nome_usuario, senha):
        dados = [nome_usuario, senha]

        dql = f"""
            SELECT f.id, p.nome, f.tipoFunc_id
            FROM funcionarios f
            INNER JOIN pessoas p 
                ON p.id = f.pessoa_id
            INNER JOIN logins l
                ON l.funcionario_id = f.id 
                AND (l.nome_usuario = ? AND l.senha = ?);
        """

        with conn:
            conn_cursor.execute(dql, dados)
            dados_usuario = conn_cursor.fetchone()

        return dados_usuario


class Pessoa:
    @staticmethod
    def fazer_login(conn, conn_cursor, username, senha):
        return database.validar_login(conn, conn_cursor, username, senha)

    @staticmethod
    def sair_conta():
        pass


class Administrador(Pessoa):
    def __init__(self, id_admin, nome):
        self.__id = id_admin
        self.__nome = nome

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    def consultar_administradores(self,tipo):
        self.tipo = tipo
        query=f"""  
                SELECT pessoas.nome
                FROM pessoas
                INNER JOIN funcionarios
                ON funcionarios.id=pessoas.id
                WHERE funcionarios.tipoFunc_id = {tipo};   
                """        
        with conn:
            cursor.execute(query)
            data = cursor.fetchall()
            return data


    def consultar_funcionarios(self):
        query="""  
                SELECT pessoas.nome
                FROM pessoas
                INNER JOIN funcionarios
                ON funcionarios.id=pessoas.id
                WHERE funcionarios.tipoFunc_id = 0;   
                """               

    def cadastrar_administradores(self):
        pass

    def cadastrar_funcionarios(self):
        pass

    def atualizar_administradores(self):
        pass

    def atualizar_funcionarios(self):
        pass

    def deletar_administradores(self):
        pass

    def deletar_funcionarios(self):
        pass



class Funcionario(Pessoa):
    def __init__(self, id, nome):
        self.__id = id
        self.__nome = nome

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    def sair_conta(self):
        pass


class Movimentacao(ABC):
    @abstractmethod
    def deletar_produto(self):
        pass

    @abstractmethod
    def inserir_produto(self):
        pass

    @abstractmethod
    def alterar_produto(self):
        pass

    @abstractmethod
    def consultar_produto(self):
        pass


class Venda(Movimentacao):
    def deletar_produto(self):
        pass

    def inserir_produto(self):
        pass

    def alterar_produto(self):
        pass

    def consultar_produto(self):
        pass

    def gerar_nota_fiscal(self):
        pass


class Estoque(Movimentacao):
    def deletar_produto(self):
        pass

    def inserir_produto(self):
        pass

    def alterar_produto(self):
        pass

    def consultar_produto(self):
        pass
