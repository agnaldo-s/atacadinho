def tabelas(conn, conn_cursor):
    ddl = """
        CREATE TABLE IF NOT EXISTS pessoas(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nome VARCHAR(70) NOT NULL,
            cpf VARCHAR(11) NOT NULL UNIQUE,
            dt_nasc DATE NOT NULL,
            telefone VARCHAR(13) NOT NULL,
            email VARCHAR(60) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS funcionarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            matricula VARCHAR(6) NOT NULL,
            dt_cadastro DATE NOT NULL,
            pessoa_id INT NOT NULL,
            CONSTRAINT fk_funcionario_pessoa
                FOREIGN KEY(pessoa_id)
                REFERENCES pessoas(id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS administradores(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            matricula VARCHAR(6) NOT NULL,
            dt_cadastro DATE NOT NULL,
            pessoa_id INT NOT NULL,
            CONSTRAINT fk_administrador_pessoa
                FOREIGN KEY(pessoa_id)
                REFERENCES pessoas(id)
        );
        CREATE TABLE IF NOT EXISTS logins(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nome_usuario VARCHAR(60) NOT NULL,
            senha VARCHAR(60) NOT NULL,
            perfil VARCHAR(13) NOT NULL,
            administrador_id INT NULL,
            funcionario_id INT NULL,
            CONSTRAINT fk_login_administrador
                FOREIGN KEY(administrador_id)
                REFERENCES administradores(id)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            CONSTRAINT fk_login_funcionario
                FOREIGN KEY(funcionario_id)
                REFERENCES funcionarios(id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );
    """

    with conn:
        conn_cursor.executescript(ddl)


def validar_login(conn, conn_cursor, username, senha):
    login = [username, senha]

    dql = """
        SELECT * FROM logins
        WHERE nome_usuario = ? AND senha = ?;
    """

    with conn:
        conn_cursor.execute(dql, login)

        dados_login = conn_cursor.fetchone()

    print(dados_login)