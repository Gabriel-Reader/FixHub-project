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


# Função para verificar login
def verificar_login(usuario, senha):
    cursor_obj = conn.cursor()
    cursor_obj.execute(
        """
            SELECT id_morador, senha FROM morador WHERE nome = %s
        """, (usuario,)
    )
    resultado = cursor_obj.fetchone()
    if resultado:
        id_morador, senha_armazenada = resultado
        if senha == senha_armazenada:
            cursor_obj.close()
            return id_morador  # Retorna id_morador para uso na sessão
    return False

def criar_pedido(pedido):
    cursor_obj = conn.cursor()
    cursor_obj.execute(
        """
            INSERT INTO pedidos (
                id, id_morador, categoria, local_manuntencao, 
                ala, ceu_quarto, descricao, comentario_gestor, 
                status, data_criacao
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, pedido
    )
    conn.commit()
    cursor_obj.close()