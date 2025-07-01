from flask import Flask, request, render_template, flash, redirect, url_for, session
from validacoes import validar_email, validar_password, validar_username

# --- Configuração da Aplicação Flask ---
app = Flask(__name__)
app.secret_key = 'Reader632' # Chave para sessões e mensagens flash.

# --- Definição de Rotas da Aplicação ---

@app.route('/', methods=['GET', 'POST'])
def tela_login():
    """
    Rota para a tela de login.
    Processa a submissão do formulário de login e redireciona.
    """
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        senha = request.form.get('senha', '').strip()
        erro = False

        # TODO: Verificar dados do login no banco de dados.

        if erro:
            return redirect(url_for('tela_login'))
        else:
            # flash('Login bem-sucedido!')
            return redirect(url_for('tela_cadastro'))

    return render_template('index.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def tela_cadastro():
    """
    Rota para a tela de cadastro de novos usuários.
    Processa a submissão do formulário de cadastro e valida os dados.
    """
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


@app.route('/painel-morador')
def painel_morador():
    return render_template('painelMorador.html')

@app.route('/painel-gestor')
def painel_gestor():   
    return render_template('painelGestor.html') 





# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True) # Ativa o modo de depuração