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




@app.route('/')
def hello():
    return render_template(
        'relatorios.html',
        dados=dados
    )



app.run()
