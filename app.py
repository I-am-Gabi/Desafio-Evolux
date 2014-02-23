#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import (
    Flask, render_template, flash,
    url_for, redirect, request
)
import cgi
import os

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': '\x9a%\xc2\xc6\x80\xc7\x8e\xfd\xf0\xc1\x87\x1dl\xbc\xfc\x12\xa1\xf7\x84\\\xe3\xaa\xb5\x19',
    'DEBUG': True
})

@app.route('/')
def hello():
    return render_template("index.html")

@app.route("/form", methods=['GET', 'POST'])
def formou():
    form = cgi.FieldStorage()
    if request.method == 'POST':
        missing = validar()
        if missing:
            flash("Aviso!\n" + missing)
        else: 
            bar = { 
                'Nome': request.form.get('nome') ,
                'Endereco': request.form.get('endereco') ,
                'Especialidade': request.form.get('especialidade') ,
                'Horario de abertura': request.form.get('funcionamento_abertura') ,
                'Horario de funcionamento': request.form.get('funcionamento_fecha') 
                }

            
            with open("form.txt", "a") as text_file:
                text_file.write('\n')
                text_file.write("BAR\n")
                for k, v in bar.items(): 
                    text_file.write("%s: %s" % (k, v))
                    text_file.write('\n')

    return render_template("form.html")

@app.route("/lista", methods=['GET'])
def listar():  
    a = []
    for line in open('form.txt'): 
        a.append(line)
        a = ''.join(a)

    flash(conteudo)

    return render_template("lista.html")

def validar():
    missing = ""
    mis = False
    if not request.form.get('nome'):
        missing = "O campo nome esta em branco.\n" 
        mis = True
    if not request.form.get('endereco'):
        missing += "O campo endereco esta em branco.\n"
        mis = True
    if not request.form.get('especialidade'):
        missing += "O campo especialidade esta em branco.\n"
        mis = True
    if not request.form.get('funcionamento_abertura'):
        missing += "O campo horario de abertura esta em branco.\n"
        mis = True
    if not request.form.get('funcionamento_fecha'):
        missing += "O campo horario de fechamento esta em branco.\n"
        mis = True

        return (missing)


if __name__ == "__main__":
    app.run(debug=True)
