import pandas as pd
import numpy as np
import os

class tratamento_de_dados:
    
    def concatena_atributos(self,Exp,Pub,Con):
        X = [Exp,Pub,Con]
        return X
    
    def get_dados_gerais(self):
        Pasta_Raiz = os.getcwd()
        Pasta_Raiz = Pasta_Raiz + '\\dados'
        arquivo = "Dados_Python.xlsx"
        caminho = os.path.join(Pasta_Raiz,arquivo)
        dados_gerais = pd.read_excel(caminho, sheet_name='Dados_Python')
        dados_gerais.drop(['Salário'],axis=1)
        return dados_gerais

    def separa_dados_treino(self,dados_gerais):

        return dados_gerais
    
    def separa_dados_teste(self,dados_gerais):
        
        return dados_gerais