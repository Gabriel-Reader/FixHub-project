from conexao import conn


def criar_usuario(usuario):
    cursor_obj = conn.cursor()
    cursor_obj.execute(
            """
                INSERT INTO morador (nome, senha, email, ceu_quarto, ceu_casa)
                VALUES (%s, %s, %s, %s, %s)
            """, usuario
        )
    conn.commit()
    cursor_obj.close()


def verificar_login(usuario, senha_digitada):
    cursor_obj = conn.cursor()
    cursor_obj.execute(
        """
            SELECT id_morador, nome, senha, ceu_casa FROM morador WHERE nome = %s
        """, (usuario,)
    )
    dados_usuario_db = cursor_obj.fetchone()

    if dados_usuario_db:
        id_morador_db, nome_db, senha_db, ceu_casa_db = dados_usuario_db

        if nome_db is None:
            cursor_obj.close()
            return False

        elif senha_digitada != senha_db:
            cursor_obj.close()
            return False

        else:
            cursor_obj.close()
            return dados_usuario_db

    return False


def criar_pedido(pedido):
    cursor_obj = conn.cursor()
    cursor_obj.execute(
        """
            INSERT INTO pedidos (
                id_morador,casa, local_manuntencao, categoria,
                quarto, ala, descricao, comentario_gestor,
                status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, pedido
    )
    conn.commit()
    cursor_obj.close()


def mostrar_pedidos_morador(id_morador):
    cursor_obj = conn.cursor()
    cursor_obj.execute(
        """
            SELECT * FROM pedidos
            WHERE id_morador = %s
        """, (id_morador,)
    )
    pedidos = cursor_obj.fetchall()
    cursor_obj.close()
    return pedidos


def mostrar_pedidos_gestor():
    cursor_obj = conn.cursor()
    cursor_obj.execute(
        """
            SELECT * FROM pedidos
            ORDER BY
            CASE
                WHEN status = 'Concluido' THEN 1
                ELSE 0
            END,
            criada_em ASC
        """
    )
    pedidos = cursor_obj.fetchall()
    cursor_obj.close()
    return pedidos


    """
    -- Cria tabela morador
    CREATE TABLE morador (
        id_morador SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        senha VARCHAR(64) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        ceu_quarto INTEGER NOT NULL,
        ceu_casa VARCHAR(10),
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """


    """
    -- Cria tabela pedidos

    CREATE TABLE pedidos(
        id_pedido SERIAL,
        id_morador INTEGER REFERENCES morador(id_morador),
        casa VARCHAR(10) NOT NULL,
        categoria VARCHAR(50) NOT NULL,
        local_manuntencao VARCHAR(60),
        ala INT,
        quarto INT,
        descricao VARCHAR(2000),
        comentario_gestor VARCHAR(255),
        status VARCHAR(60),
        Criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(id_pedido)
    );
    """
