from flask import (
    Flask, render_template, flash,
    url_for, redirect, request
)
import cgi
import os

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'Evolux <3 Python',
    'DEBUG': True
})

@app.route('/<nome>')
def hello(nome):
    return "Hello World %s!" % nome

@app.route("/", methods=['GET', 'POST'])
def formou():
    if request.method == 'POST':
        if request.form.get('nome'):
            with open("form.txt", "a") as text_file:
                text_file.write(request.form.get('nome'))
                text_file.write(request.form.get('\n'))
                text_file.write(request.form.get('endereco'))
                text_file.write(request.form.get('\n'))
                text_file.write(request.form.get('especialidade'))
                text_file.write(request.form.get('\n'))
                text_file.write(request.form.get('funcionamento'))
                text_file.write(request.form.get('\n'))
        else:
            flash('Preencha todos os campos')

    return render_template("index.html").encode('utf-8')

if __name__ == "__main__":
    app.run(debug=True)
