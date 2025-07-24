# ---------------------------------------------
# FixHub - Sistema de Gestão de Pedidos (Flask)
# ---------------------------------------------

# Importações de bibliotecas Flask e módulos internos
from flask import Flask, request, render_template, flash, redirect, url_for, session
from services.manipular_database import criar_usuario, verificar_login, criar_pedido, mostrar_pedidos_morador, mostrar_pedidos_gestor, alterar_status_pedido, comentario_gestor, deletar_pedido, obter_filtros_disponiveis
from utils.validacoes import validar_email, validar_password, validar_username, verifica_gestor
from utils.utilitarios import converter_pedidos_para_dicionario
from utils.manipular_forms import obter_dados_pedido, obter_dados_cadastro, obter_dados_login, obter_atualizacao_pedido


# Instanciação da aplicação Flask e configuração da chave secreta para sessões
app = Flask(__name__)
app.secret_key = 'd2ccd1731dc1cca262d6c889e3352a921f973db9698cc4ba'


# -----------------------------
# Rota principal: Tela de login
# Permite login de usuários e redireciona conforme o tipo (gestor ou morador)
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
        # Exibe o formulário de cadastro
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
# Rota do painel do morador: permite visualizar, criar e remover pedidos
# -----------------------------
@app.route('/painel-morador', methods=['GET', 'POST'])
def painel_morador():
    if 'user_id' in session:
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
# Rota do painel do gestor: visualiza e atualiza todos os pedidos
# -----------------------------
@app.route('/painel-gestor', methods=['GET'])
def painel_gestor():
    if 'user_id' in session:
        # Obter parâmetros de filtro da URL (via request.args)
        filtro_casa = request.args.get('casa', '') # Pega o valor, padrão vazio para "Todas as Casas"
        filtro_categoria = request.args.get('categoria', '') # Padrão vazio para "Todas as Categorias"
        filtro_status = request.args.get('status', '') # Padrão vazio para "Todos os Status"
        ordenar_por = request.args.get('ordenar_por', 'recentes') # Padrão 'recentes'

        # Chamar mostrar_pedidos_gestor com os filtros
        pedidos_tuplas = mostrar_pedidos_gestor(
            filtro_casa=filtro_casa if filtro_casa else None, # Passa None se o filtro for vazio
            filtro_categoria=filtro_categoria if filtro_categoria else None,
            filtro_status=filtro_status if filtro_status else None,
            ordenar_por=ordenar_por
        )
        
        # Converter as tuplas para dicionários
        pedidos_gestor = converter_pedidos_para_dicionario(pedidos_tuplas)

        # Obter casas e categorias disponíveis para preencher os selects de filtro
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
# Inicia o servidor Flask em modo de depuração
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True) # Ativa o modo de depuração