from flask import Flask, render_template
import pandas as pd
import numpy as np
import os

#inicializa o flask
app = Flask(__name__)

#busca e trata os dados do excel
Pasta_Raiz = os.getcwd()
Pasta_Raiz = Pasta_Raiz + '\\dados'
arquivo = "Dados_Python.xlsx"

caminho = os.path.join(Pasta_Raiz,arquivo)
dados = pd.read_excel(caminho, sheet_name='Dados_Python')
dados.drop(['Salário'],axis=1)



@app.route('/')
def dados_teste():
    return render_template(
        
    )


@app.route('/dados_treino')
def dados_treino():
    return render_template(
        'dados_treino.html',
        dados=dados
    )



app.run()
