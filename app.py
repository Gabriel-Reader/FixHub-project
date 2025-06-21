from flask import Flask, request, render_template, flash, redirect, url_for

app = Flask(__name__)

app.secret_key = 'reader632'

@app.route('/', methods=['GET', 'POST'])
def tela_login():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        senha = request.form.get('senha', '').strip()
        erro = False

        if len(usuario) < 3:
            flash('* O nome de usuário deve ter pelo menos 3 caracteres.')
            erro = True
        if len(senha) < 6:
            flash('* A senha deve ter pelo menos 6 caracteres.')
            erro = True

        if erro:
            return redirect(url_for('tela_login'))
        else:
            flash('Login bem-sucedido!')
            return redirect(url_for('tela_login'))

    return render_template('index.html')
        




if __name__ == '__main__':
    app.run()