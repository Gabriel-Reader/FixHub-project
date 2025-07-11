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
            SELECT id_morador, nome, senha FROM morador WHERE nome = %s
        """, (usuario,)
    )
    dados_usuario_db = cursor_obj.fetchone()

    if dados_usuario_db:
        id_morador_db, nome_db, senha_db = dados_usuario_db

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
                casa, local_manuntencao, categoria,
                quarto, ala, descricao, comentario_gestor,
                status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, pedido
    )
    conn.commit()
    cursor_obj.close()