from flask import Flask, request, render_template, flash, redirect, url_for, session
from validacoes import validar_email, validar_password, validar_username
from datetime import datetime
import random


app = Flask(__name__)
app.secret_key = 'v5Y71oV1n7av'

pedidos_temporarios = []

# --- Definição de Rotas da Aplicação ---

@app.route('/', methods=['GET', 'POST'])
def tela_login():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        senha = request.form.get('senha', '').strip()
        erro = False

        # TODO: Verificar dados do login no banco de dados.

        if erro:
            return redirect(url_for('tela_login'))
        else:
            # flash('Login bem-sucedido!')
            return redirect(url_for('painel_morador'))

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

        # Validação dos campos de cadastro
        if not validar_username(c_usuario):
            flash('* O usuário deve ter apenas letras e números (3-20 caracteres).')
            erro = True

        if not validar_password(c_senha):
            flash('* A senha deve ter pelo menos 6 caracteres, incluindo letras e números.')
            erro = True

        if not validar_email(c_email):
            flash('* Insira um E-mail válido.')
            erro = True

        # TODO: Salvar os dados no banco de dados.

        if erro:
            return redirect(url_for('tela_cadastro'))
        else:
            # flash('Cadastro bem-sucedido!')
            return redirect(url_for('tela_login'))



@app.route('/painel-morador', methods=['GET', 'POST'])
def painel_morador():
    if 'pedidos' not in session: # verifica se a lista pedidos foi criada 
        session['pedidos'] = []

    if request.method == 'POST':
        novo_pedido = {
            'id': f'#{random.randint(1, 100000)}',
            'casa': request.form.get('m_casa'),
            'local': request.form.get('m_localManutencao'),
            'categoria': request.form.get('m_categoria'),
            'quarto': request.form.get('m_quarto'),
            'ala': request.form.get('m_ala'),
            'descricao': request.form.get('m_descricao'),
            'data_criacao': datetime.now().strftime('%d/%m/%Y'),
            'status': 'Aberto',
            'comentario_gestor': 'Nenhum comentário ainda.'
        }

        # lista temporária para desenvolver o painel do gestor (depois será removido)
        pedidos_temporarios.insert(0, novo_pedido)
        
        # salva o dic de info dos pedidos na sessão do usuário
        pedidos_atualizados = session['pedidos']
        pedidos_atualizados.insert(0, novo_pedido)
        session['pedidos'] = pedidos_atualizados

        return redirect(url_for('painel_morador'))

    # recupera o dic de infos do pedido e retornar para o HTML
    pedidos = session.get('pedidos', [])
    return render_template('painelMorador.html', pedidos=pedidos)



@app.route('/painel-gestor', methods=['GET', 'POST'])
def painel_gestor():
    return render_template('painelGestor.html', pedidos=pedidos_temporarios)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('tela_login'))



# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True) # Ativa o modo de depuração