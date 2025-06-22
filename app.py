from flask import Flask, request, render_template, flash, redirect, url_for
import re

app = Flask(__name__)

app.secret_key = 'Reader632' # chave para 'flash' funcionar e garantir segurança ao Flask


def usuario_valido(usuario):
    return re.fullmatch(r'^[a-zA-Z0-9_]{3,20}$', usuario) is not None

def senha_valida(senha):
    # Pelo menos 6 caracteres, pelo menos uma letra e um número
    return re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$', senha) is not None


@app.route('/', methods=['GET', 'POST'])
def tela_login():
    if request.method == 'POST':
        # recuperando dados com base no 'name' do HTML
        usuario = request.form.get('usuario', '').strip()
        senha = request.form.get('senha', '').strip()
        erro = False

        if not usuario_valido(usuario):
            flash('* O usuário deve ter apenas letras e números (3-20 caracteres).')
            erro = True

        if not senha_valida(senha):
            flash('* A senha deve ter pelo menos 6 caracteres, incluindo letras e números.')
            erro = True

        if erro:
            return redirect(url_for('tela_login'))
        else:
            flash('Login bem-sucedido!')
            # trocar pela página que será direcionada ao fazer login
            return redirect(url_for('tela_login'))

    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def tela_cadastro():
    return render_template('cadastro.html')



if __name__ == '__main__':
    app.run()