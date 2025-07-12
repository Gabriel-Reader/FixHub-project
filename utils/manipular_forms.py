from flask import request, session

def obter_dados_pedido():
    casa = request.form.get('m_casa').strip()
    categoria = request.form.get('m_categoria').strip()
    local = request.form.get('m_localManutencao').strip()
    ala = request.form.get('m_ala').strip()
    quarto = request.form.get('m_quarto').strip()
    descricao = request.form.get('m_descricao').strip()
    comentario_gestor = 'Nenhum comentário ainda.'.strip()
    status = 'Aberto'.strip()
    id_morador = session.get('user_id')

    return [id_morador, casa, categoria, local, ala, quarto, descricao, comentario_gestor, status]

def obter_dados_cadastro():
    c_usuario = request.form.get('c_usuario').strip()
    c_email = request.form.get('c_email').strip()
    c_senha = request.form.get('c_senha').strip()
    c_quarto = request.form.get('c_quarto').strip()
    c_casa = request.form.get('c_casa').strip()

    return [c_usuario, c_email, c_senha, c_quarto, c_casa]

def obter_dados_login():
    usuario = request.form.get('usuario').strip()
    senha = request.form.get('senha').strip()

    return [usuario, senha]

def obter_atualizacao_pedido():
    pedido_id = request.form.get('pedido_id')
    novo_status = request.form.get('status')
    novo_comentario = request.form.get('comentario')

    return [pedido_id, novo_status, novo_comentario]