from services.conexao import conn
from datetime import datetime


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

def mostrar_pedidos_gestor(filtro_casa=None, filtro_categoria=None, filtro_status=None, ordenar_por='recentes'):
    cursor_obj = conn.cursor()
    sql = """
        SELECT p.*, m.nome AS nome_morador
        FROM pedidos p
        JOIN morador m ON p.id_morador = m.id_morador
    """
    parametros = []
    where_clauses = []

    # Adiciona cláusulas WHERE com base nos filtros fornecidos
    if filtro_casa:
        where_clauses.append("p.casa = %s")
        parametros.append(filtro_casa)
    if filtro_categoria:
        where_clauses.append("p.categoria = %s")
        parametros.append(filtro_categoria)
    if filtro_status:
        where_clauses.append("p.status = %s")
        parametros.append(filtro_status)

    # Constrói a cláusula WHERE final
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    # Adiciona a cláusula ORDER BY com base na opção de ordenação
    if ordenar_por == 'status':
        sql += """
            ORDER BY
            CASE
                WHEN p.status = 'Concluído' THEN 1
                ELSE 0
            END,
            p.criada_em ASC
        """
    else: # Padrão: 'recentes'
        sql += " ORDER BY p.criada_em DESC" # Ordena por data de criação decrescente (mais recentes primeiro)

    cursor_obj.execute(sql, tuple(parametros))
    pedidos = cursor_obj.fetchall()
    cursor_obj.close() # Garante que o cursor seja fechado antes do retorno
    return pedidos


def obter_filtros_disponiveis():
    """
    Busca todas as casas (CEU) e categorias únicas existentes no banco de dados
    para popular os dropdowns de filtro no frontend.

    Returns:
        tuple: Uma tupla contendo duas listas: (casas_disponiveis, categorias_disponiveis).
               Retorna listas vazias em caso de erro.
    """
    cursor_obj = conn.cursor()
    casas = []
    categorias = []
    
    # Busca casas únicas da tabela 'morador'
    cursor_obj.execute("SELECT DISTINCT ceu_casa FROM morador WHERE ceu_casa IS NOT NULL ORDER BY ceu_casa ASC")
    casas = [row[0] for row in cursor_obj.fetchall()]

    # Busca categorias únicas da tabela 'pedidos'
    cursor_obj.execute("SELECT DISTINCT categoria FROM pedidos WHERE categoria IS NOT NULL ORDER BY categoria ASC")
    categorias = [row[0] for row in cursor_obj.fetchall()]
    
    cursor_obj.close() # Garante que o cursor seja fechado antes do retorno
    return casas, categorias

def alterar_status_pedido(id_pedido, novo_status):
    cursor_obj = conn.cursor()
    cursor_obj.execute(
        """
            UPDATE pedidos
            SET status = %s
            WHERE id_pedido = %s
        """, (novo_status, id_pedido)
    )
    conn.commit()
    cursor_obj.close()


def comentario_gestor(id_pedido, novo_comentario):
    cursor_obj = conn.cursor()

    # Recupera o comentário existente
    cursor_obj.execute(
        """
            SELECT comentario_gestor FROM pedidos
            WHERE id_pedido = %s
        """, (id_pedido,)
    )
    comentario_antigo = cursor_obj.fetchone()[0] or ""

    # Cria o novo comentário com data e hora
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    comentario_atualizado = f"{comentario_antigo}\n{data_hora_atual} - {novo_comentario}"

    cursor_obj.execute(
        """
            UPDATE pedidos
            SET comentario_gestor = %s
            WHERE id_pedido = %s
        """, (comentario_atualizado, id_pedido)
    )
    conn.commit()
    cursor_obj.close()


def deletar_pedido(id_pedido, id_morador):
    cursor_obj = conn.cursor()
    cursor_obj.execute(
        """
            DELETE FROM pedidos
            WHERE id_pedido = %s AND id_morador = %s
        """, (id_pedido, id_morador)
    )
    conn.commit()
    cursor_obj.close()


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
