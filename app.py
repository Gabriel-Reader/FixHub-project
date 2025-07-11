from os import stat
from flask import Flask, request, render_template, flash, redirect, url_for, session
from manipular_database import criar_usuario, verificar_login, criar_pedido, verifica_gestor, mostrar_pedidos_morador, mostrar_pedidos_gestor
from validacoes import validar_email, validar_password, validar_username
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'd2ccd1731dc1cca262d6c889e3352a921f973db9698cc4ba'

# --- Definição de Rotas da Aplicação ---

@app.route('/', methods=['GET', 'POST'])
def tela_login():
    if request.method == 'POST':
        usuario_form = request.form.get('usuario', '').strip()
        senha_form = request.form.get('senha', '').strip()

        # Verifica se os campos estão preenchidos
        if not usuario_form or not senha_form:
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('tela_login'))

        # Verifica as credenciais no banco de dados e as retorna
        dados_usuario_db = verificar_login(usuario_form, senha_form)
        
        if dados_usuario_db:
            id_morador_db, nome_db, senha_db, ceu_casa_db = dados_usuario_db

            # LOGIN BEM-SUCEDIDO: CRIAR A SESSÃO COOKIE
            session.clear()
            session['user_id'] = id_morador_db
            session['username'] = nome_db
            session['ceu'] = ceu_casa_db

            if verifica_gestor(nome_db):
                return redirect(url_for('painel_gestor'))
            else:
                return redirect(url_for('painel_morador'))
        
        else:
            flash('Usuário ou senha incorretos.')
            return redirect(url_for('tela_login'))

    return render_template('index.html')



@app.route('/cadastro', methods=['GET', 'POST'])
def tela_cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')

    elif request.method == 'POST':
        c_usuario = request.form.get('c_usuario').strip()
        c_email = request.form.get('c_email').strip()
        c_senha = request.form.get('c_senha').strip()
        c_quarto = request.form.get('c_quarto').strip()
        c_casa = request.form.get('c_casa').strip()
        erro = False

        user = [c_usuario,c_senha,c_email,c_quarto,c_casa]

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

        if erro:
            return redirect(url_for('tela_cadastro'))
        else:
            # flash('Cadastro bem-sucedido!')
            criar_usuario(user) # Chama função e crie um novo usuario
            return redirect(url_for('tela_login'))



@app.route('/painel-morador', methods=['GET', 'POST'])
def painel_morador():
    if 'user_id' in session:
        # flash(f'Logado como {session["username"]} (ID: {session["user_id"]})')

        if request.method == 'POST':
            # novo_pedido = {
            #     'id': f'#{random.randint(1, 100000)}',
            #     'casa': request.form.get('m_casa'),
            #     'local': request.form.get('m_localManutencao'),
            #     'categoria': request.form.get('m_categoria'),
            #     'quarto': request.form.get('m_quarto'),
            #     'ala': request.form.get('m_ala'),
            #     'descricao': request.form.get('m_descricao'),
            #     'data_criacao': datetime.now().strftime('%d/%m/%Y'),
            #     'status': 'Aberto',
            #     'comentario_gestor': 'Nenhum comentário ainda.'
            # }

            #Criando o pedido e colocando no banco de dados
            casa = request.form.get('m_casa')
            categoria = request.form.get('m_categoria')
            local = request.form.get('m_localManutencao')
            ala = request.form.get('m_ala')
            quarto = request.form.get('m_quarto')
            descricao = request.form.get('m_descricao')
            comentario_gestor = 'Nenhum comentário ainda.'
            status = 'Aberto'

            pedido = [casa,categoria,local,ala,quarto,descricao,comentario_gestor,status]
            criar_pedido(pedido)

            return redirect(url_for('painel_morador'))

        # salva os pedidos na sessão
        id_morador = session.get('user_id')
        pedidos = mostrar_pedidos_morador(id_morador)
        nome_usuario = session.get('username')
        ceu_casa = session.get('ceu')

        #TODO: Os pedidos são enviados aqui
        return render_template('painelMorador.html', pedidos=pedidos, nome_usuario=nome_usuario, ceu_casa=ceu_casa)
    
    else:
        return '<body style="background:white; text-align:center;"><h1> Você não está logado </h1></body>'



@app.route('/painel-gestor', methods=['GET', 'POST'])
def painel_gestor():
    if 'user_id' in session:
        pedidos_gestor = mostrar_pedidos_gestor()
        nome_usuario = session.get('username')
        return render_template('painelGestor.html', pedidos=pedidos_gestor, nome_usuario=nome_usuario)
    else:
        return '<body style="background:white; text-align:center;"><h1> Você não está logado </h1></body>'



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('tela_login'))



# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True) # Ativa o modo de depuração
