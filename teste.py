import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split


Pasta_Raiz = os.getcwd()
Pasta_Raiz = Pasta_Raiz + '\\Dados'
arquivo = "Dados_Python.xlsx"

caminho = os.path.join(Pasta_Raiz,arquivo)

teste = pd.read_excel(caminho, sheet_name='Dados_Python')

teste.head()
print(teste)