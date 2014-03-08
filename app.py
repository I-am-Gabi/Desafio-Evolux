#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from contextlib import closing
import sqlite3

from flask import (
    Flask, render_template, flash,
    url_for, redirect, request, session, g, abort
)
import cgi
import os

app = Flask(__name__)

app.config.update(dict(
    # configuration
    DATABASE = os.path.join(app.root_path, 'flaskr.db'),
    DEBUG = True,
    SECRET_KEY = '\x9a%\xc2\xc6\x80\xc7\x8e\xfd\xf0\xc1\x87\x1dl\xbc\xfc\x12\xa1\xf7\x84\\\xe3\xaa\xb5\x19',
    USERNAME = 'admin',
    PASSWORD = 'default'
))

def connect_db():
    '''conetar meu banco de dados'''
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/form')
def form(): 
    return render_template("form.html")

@app.route("/add_bar", methods=['GET', 'POST'])
def add_bar(): 
    missing = validar() 
    if missing:
        flash("Aviso!\n" + missing)
        return render_template("form.html")
    else:
        g.db.execute('insert into bares (nome, descricao, endereco, especialidade, telefone) values (?, ?, ?, ?, ?)',
                     [request.form['nome'], request.form['descricao'], request.form['endereco'], request.form['especialidade'], request.form['telefone']])
        g.db.commit()
        flash('New bar was successfully posted')
        return render_template('lista.html')

@app.route("/lista", methods=['GET'])
def listar():  
    bar = g.db.execute('select nome, descricao, endereco, especialidade, telefone from bares order by id desc')
    bares = [dict(nome=row[0], descricao=row[1], endereco=row[2], especialidade=row[3], telefone=row[4]) for row in bar.fetchall()]
    return render_template('lista.html', bares=bares)

def validar():
    missing = ""
    mis = False
    if not request.form.get('nome'):
        missing = "O campo nome esta em branco.\n" 
    if not request.form.get('endereco'):
        missing += "O campo endereco esta em branco.\n"
    if not request.form.get('especialidade'):
        missing += "O campo especialidade esta em branco.\n"
    if not request.form.get('descricao'):
        missing += "O campo descricao esta em branco.\n"
    if not request.form.get('telefone'):
        missing += "O campo telefone esta em branco.\n"

        return missing


if __name__ == "__main__":
    app.run(debug=True)
