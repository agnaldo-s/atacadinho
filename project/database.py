def tabelas(conn, cursor):
    ddl = """
        CREATE TABLE IF NOT EXISTS pessoas(
            id INT PRIMARY KEY AUTOINCREMENT NOT NULL,
            nome VARCHAR(70) NOT NULL,
            cpf VARCHAR(11) NOT NULL UNIQUE,
            dt_nasc DATE NOT NULL,
            telefone VARCHAR(13) NOT NULL,
            email VARCHAR(60) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS funcionarios(
            id INT PRIMARY KEY AUTOINCREMENT NOT NULL,
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
            id INT PRIMARY KEY AUTOINCREMENT NOT NULL,
            matricula VARCHAR(6) NOT NULL,
            dt_cadastro DATE NOT NULL,
            pessoa_id INT NOT NULL,
            CONSTRAINT fk_administrador_pessoa
                FOREIGN KEY(pessoa_id)
                REFERENCES pessoas(id)
        );
        CREATE TABLE IF NOT EXISTS logins(
            id INT PRIMARY KEY AUTOINCREMENT NOT NULL,
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
