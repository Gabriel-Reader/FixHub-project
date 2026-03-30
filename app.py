# ---------------------------------------------
# FixHub - Sistema de Gestão de Pedidos (Flask)
# ---------------------------------------------

# Importações de bibliotecas Flask e módulos internos
from flask import Flask, request, render_template, flash, redirect, url_for, session
from services.manipular_database import (
    criar_usuario, verificar_login, criar_pedido, 
    mostrar_pedidos_morador, mostrar_pedidos_gestor, 
    mostrar_pedidos_representante, alterar_status_pedido, 
    comentario_gestor, deletar_pedido, obter_filtros_disponiveis
)
from utils.validacoes import validar_email, validar_password, validar_username, verifica_gestor, verifica_representante
from utils.utilitarios import converter_pedidos_para_dicionario
from utils.manipular_forms import obter_dados_pedido, obter_dados_cadastro, obter_dados_login, obter_atualizacao_pedido


# Instanciação da aplicação Flask e configuração da chave s. para sessões
app = Flask(__name__)
app.secret_key = 'd2ccd1731dc1cca262d6c889e3352a921f973db9698cc4ba'


# -----------------------------
# Rota principal: Tela de login
# Permite login de usuários e redireciona conforme o tipo
# -----------------------------
@app.route('/', methods=['GET', 'POST'])
def tela_login():
    if request.method == 'POST':
        # Obtém dados do formulário de login
        dados_login = obter_dados_login()
        usuario_form, senha_form = dados_login

        # Verifica as credenciais no banco de dados
        dados_usuario_db = verificar_login(usuario_form, senha_form)

        if dados_usuario_db:
            id_morador_db, nome_db, senha_db, ceu_casa_db = dados_usuario_db

            # Login bem-sucedido: cria sessão do usuário
            session.clear()
            session['user_id'] = id_morador_db
            session['username'] = nome_db
            session['ceu'] = ceu_casa_db

            # Redireciona para o painel adequado
            if verifica_gestor(nome_db):
                return redirect(url_for('painel_gestor'))
            elif verifica_representante(nome_db):
                return redirect(url_for('painel_representante'))
            else:
                return redirect(url_for('painel_morador'))

        else:
            # Falha no login
            flash('Usuário ou senha incorretos.')
            return redirect(url_for('tela_login'))

    # Renderiza a página de login
    return render_template('index.html')



# -----------------------------
# Rota de cadastro de novo usuário
# -----------------------------
@app.route('/cadastro', methods=['GET', 'POST'])
def tela_cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')

    elif request.method == 'POST':
        # Processa o formulário de cadastro
        erro = False
        user = obter_dados_cadastro()
        c_usuario, c_senha,c_email, c_quarto, c_casa = user

        # Validação dos campos de cadastro
        if not validar_username(c_usuario):
            flash('* O usuário deve ter apenas letras e números (3-20 caracteres).')
            erro = True

        if not validar_password(c_senha):
            flash('* A senha deve ter pelo menos 6 caracteres, incluindo letras e números.')
            erro = True

        if not validar_email(c_email):
            flash('*Insira um E-mail válido.')
            erro = True

        # Se houver erro, retorna para o formulário com mensagens
        if erro:
            return render_template('cadastro.html', user_data=user)
        else:
            # Cadastro bem-sucedido: cria novo usuário
            criar_usuario(user)
            return redirect(url_for('tela_login'))



# -----------------------------
# Rota do painel do morador
# -----------------------------
@app.route('/painel-morador', methods=['GET', 'POST'])
def painel_morador():
    if 'user_id' in session:
        username = session.get('username')
        # Verifica se o usuário logado NÃO é um gestor ou representante
        if verifica_gestor(username):
            return redirect(url_for('painel_gestor'))
        if verifica_representante(username):
            return redirect(url_for('painel_representante'))

        # Usuário autenticado
        if request.method == 'POST':
            # Criação de novo pedido
            pedido = obter_dados_pedido()
            criar_pedido(pedido)
            return redirect(url_for('painel_morador'))

        # Busca pedidos do morador logado
        id_morador = session.get('user_id')
        pedidos_tuplas = mostrar_pedidos_morador(id_morador)
        pedidos = converter_pedidos_para_dicionario(pedidos_tuplas)

        nome_usuario = session.get('username')
        ceu_casa = session.get('ceu')

        # Renderiza painel do morador com os pedidos
        return render_template('painelMorador.html', pedidos=pedidos, nome_usuario=nome_usuario, ceu_casa=ceu_casa)

    else:
        # Usuário não autenticado
        return redirect(url_for('unauthorized'))



# -----------------------------
# Rota do painel do representante
# -----------------------------
@app.route('/painel-representante', methods=['GET'])
def painel_representante():
    if 'user_id' in session:
        if not verifica_representante(session.get('username')):
            return redirect(url_for('unauthorized'))

        filtro_casa = request.args.get('casa', '')
        filtro_status = request.args.get('status', '')
        
        pedidos_tuplas = mostrar_pedidos_representante(
            filtro_casa=filtro_casa if filtro_casa else None,
            filtro_status=filtro_status if filtro_status else None
        )
        pedidos = converter_pedidos_para_dicionario(pedidos_tuplas)
        
        casas_disponiveis, _ = obter_filtros_disponiveis()
        nome_usuario = session.get('username')

        return render_template(
            'painelRepresentante.html',
            pedidos=pedidos,
            nome_usuario=nome_usuario,
            casas_disponiveis=casas_disponiveis,
            filtro_casa=filtro_casa,
            filtro_status=filtro_status
        )
    else:
        return redirect(url_for('unauthorized'))



# -----------------------------
# Rota para o representante aprovar ou recusar pedido
# -----------------------------
@app.route('/acao-representante', methods=['POST'])
def acao_representante():
    if 'user_id' in session and verifica_representante(session.get('username')):
        pedido_id = request.form.get('pedido_id')
        acao = request.form.get('acao') # 'aprovar', 'recusar', 'deletar'
        comentario = request.form.get('comentario')

        # Se houver comentário, salva no histórico
        if comentario:
            comentario_gestor(pedido_id, f"[REPRESENTANTE]: {comentario}")

        if acao == 'aprovar':
            alterar_status_pedido(pedido_id, 'Aberto')
        elif acao == 'recusar':
            alterar_status_pedido(pedido_id, 'Recusado pelo Representante')
        elif acao == 'deletar':
            # Para deletar, precisamos do id do morador dono do pedido, 
            # ou criar uma função de deletar genérica.
            # Vou usar uma alteração de status para "Removido" ou similar por segurança,
            # ou buscar o id_morador. Vamos usar uma função de delete por ID apenas.
            cursor_obj = conn.cursor()
            cursor_obj.execute("DELETE FROM pedidos WHERE id_pedido = %s", (pedido_id,))
            conn.commit()
            cursor_obj.close()
            
        return redirect(url_for('painel_representante'))
    else:
        return redirect(url_for('unauthorized'))



# -----------------------------
# Rota do painel do gestor
# -----------------------------
@app.route('/painel-gestor', methods=['GET'])
def painel_gestor():
    if 'user_id' in session:
        # Verifica se o usuário logado é um gestor
        if not verifica_gestor(session.get('username')):
            return redirect(url_for('unauthorized'))

        # Obter parâmetros de filtro da URL (via request.args)
        filtro_casa = request.args.get('casa', '')
        filtro_categoria = request.args.get('categoria', '')
        filtro_status = request.args.get('status', '')
        ordenar_por = request.args.get('ordenar_por', 'recentes')

        pedidos_tuplas = mostrar_pedidos_gestor(
            filtro_casa=filtro_casa if filtro_casa else None,
            filtro_categoria=filtro_categoria if filtro_categoria else None,
            filtro_status=filtro_status if filtro_status else None,
            ordenar_por=ordenar_por
        )
        
        pedidos_gestor = converter_pedidos_para_dicionario(pedidos_tuplas)
        casas_disponiveis, categorias_disponiveis = obter_filtros_disponiveis()
        nome_usuario = session.get('username')

        return render_template(
            'painelGestor.html',
            pedidos=pedidos_gestor,
            nome_usuario=nome_usuario,
            filtro_casa=filtro_casa,
            filtro_categoria=filtro_categoria,
            filtro_status=filtro_status,
            filtro_ordenar_por=ordenar_por,
            casas_disponiveis=casas_disponiveis,
            categorias_disponiveis=categorias_disponiveis
        )
    else:
        # Usuário não autenticado
        return redirect(url_for('unauthorized'))



# -----------------------------
# Rota para atualizar o status e comentário de um pedido (gestor)
# -----------------------------
@app.route('/atualizar-pedido', methods=['POST'])
def atualizar_pedido():
    if request.method == 'POST':
        if 'user_id' in session:
            # Verifica se o usuário logado é um gestor
            if not verifica_gestor(session.get('username')):
                return redirect(url_for('unauthorized'))

            # Obtém dados do formulário de atualização
            novos_dados_pedido = obter_atualizacao_pedido()
            pedido_id, novo_status, novo_comentario = novos_dados_pedido

            # Atualiza status e comentário do pedido
            alterar_status_pedido(pedido_id, novo_status)
            comentario_gestor(pedido_id, novo_comentario)
            return redirect(url_for('painel_gestor'))
        else:
            return redirect(url_for('unauthorized'))



# -----------------------------
# Rota para deletar um pedido (morador)
# -----------------------------
@app.route('/deletar-pedido/<int:id_pedido>', methods=['POST'])
def deletar_pedido_rota(id_pedido):
    if 'user_id' in session:
        # Verifica se o usuário logado NÃO é um gestor ou representante
        username = session.get('username')
        if verifica_gestor(username) or verifica_representante(username):
            return redirect(url_for('unauthorized'))

        id_morador = session.get('user_id')
        deletar_pedido(id_pedido, id_morador)
        return redirect(url_for('painel_morador'))
    else:
        return redirect(url_for('unauthorized'))



# -----------------------------
# Rota para logout do usuário
# -----------------------------
@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.clear()
        return redirect(url_for('tela_login'))



# -----------------------------
# Rota para acesso não autorizado
# -----------------------------
@app.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html')



# -----------------------------
# Execução da Aplicação
# -----------------------------
if __name__ == '__main__':
    from services.conexao import conn # Garantir que a conexão está disponível
    app.run(debug=True)
