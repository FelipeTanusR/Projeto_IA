from flask import Flask, render_template, url_for, flash, request, redirect
from services import tratamento_de_dados
import pandas as pd
import numpy as np
import os

#inicializa o objeto de tratamento de dados
action = tratamento_de_dados()

#inicializa o flask
app = Flask(__name__)
app.secret_key = 'Projeto_IA'

#busca e trata os dados do excel
dados_gerais = action.get_dados_gerais()
dados_para_treino = action.separa_dados_treino(dados_gerais)
dados_para_teste = action.separa_dados_teste(dados_gerais)





########################################################
##################PAGINA PRINCIPAL######################
@app.route('/')
def inicio():
    
    return redirect(url_for('home'))

@app.route('/home')
def home():
    
    return render_template(
        'home.html'
    )

@app.route('/testar_curriculo',methods=['POST'])
def testar_curriculo():
    try:
        exp = request.form['exp']
        pub = request.form['pub']
        con = request.form['con']

        X = action.concatena_atributos(exp,pub,con)
        print(X)

        flash(X, 'SUCESSO_1')
        return redirect(url_for('home'))
    except Exception as e:
        flash('Erro ao realizar ação.', 'ERRO_1')
        return redirect(url_for('home'))


########################################################
##################PAGINAS DE DADOS######################
@app.route('/dados_treino')
def dados_treino():
    return render_template(
        'dados_treino.html',
        dados=dados_para_treino
    )

@app.route('/dados_teste')
def dados_teste():
    return render_template(
        'dados_teste.html',
        dados=dados_para_teste
    )



app.run()
