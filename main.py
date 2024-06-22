from flask import Flask, render_template, url_for, flash, request, redirect
from services import tratamento_de_dados
from sklearn import datasets
from sklearn.model_selection import train_test_split
from KNN import KNN
import pandas as pd
import numpy as np
import os

#inicializa o objeto de tratamento de dados
action = tratamento_de_dados()

#inicializa o flask
app = Flask(__name__)
app.secret_key = 'Projeto_IA'

#busca os dados do arquivo excel
dados_gerais = action.get_dados_gerais()


#converte os dados para tuplas x,y


X = action.get_x(dados_gerais)
Y = action.get_y(dados_gerais)


#separa os casos de teste e treino
treino_x, teste_x, treino_y, teste_y =  train_test_split(X.to_numpy(),Y.to_numpy(), test_size= 0.2, random_state=1234)



clf = KNN()
clf.fit(treino_x,treino_y)
teste_y = clf.predict(teste_x)



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
        dados=action.get_dados(treino_x,treino_y)
    )

@app.route('/dados_teste')
def dados_teste():
    return render_template(
        'dados_teste.html',
        dados=action.get_dados(teste_x,teste_y)
    )



app.run()
