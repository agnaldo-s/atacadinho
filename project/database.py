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

        CREATE TABLE IF NOT EXISTS tiposFuncionarios(
            id_tipoFunc INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            descricao VARCHAR(70) NOT NULL                        
        );

        CREATE TABLE IF NOT EXISTS funcionarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            matricula VARCHAR(6) NOT NULL,
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
            perfil VARCHAR(13) NOT NULL,
            administrador_id INTEGER NULL,
            funcionario_id INTEGER NULL,
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
        
        CREATE TABLE IF NOT EXISTS categorias(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            descricao VARCHAR(255) NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS produtos(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nome VARCHAR(60) NOT NULL,
            valor_unitario DECIMAL(10,2),
            administrador_id INTEGER NOT NULL,
            categoria_id INTEGER NOT NULL,
            CONSTRAINT fk_produtos_administradores
                FOREIGN KEY(administrador_id)
                REFERENCES administradores(id)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            CONSTRAINT fk_produtos_categorias
                FOREIGN KEY(categoria_id)
                REFERENCES categorias(id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );
    
        CREATE TABLE IF NOT EXISTS regitro_movimentacao(
            id_regMovitacao INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS estoque(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            id_regMovitacao INTEGER NOT NULL,
            data_hora DATETIME default current_timestamp,
            id_funcionario INTERGER NOT NULL,
            CONSTRAINT fk_estoque_registro_movimentacao
                FOREIGN KEY(id_regMovitacao)
                REFERENCES regitro_movimentacao(id_regMovitacao),
            CONSTRAINT fk_estoque_funcionarios
                FOREIGN KEY(id_funcionario)
                REFERENCES funcionarios(id)
            CONSTRAINT fk_estoque_produtos
                FOREIGN KEY(produto_id)
                REFERENCES produtos(id)
        );



    """
