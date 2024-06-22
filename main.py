from flask import Flask, render_template, url_for, flash, request, redirect
from Services import tratamento_de_dados
from sklearn.model_selection import train_test_split
import numpy as np
from KNN import KNN

#inicializa o flask
app = Flask(__name__)
app.secret_key = 'Projeto_IA'

#inicializa o objeto de tratamento de dados
action = tratamento_de_dados()

#busca os dados do arquivo excel
dados_gerais = action.get_dados_gerais()
print(dados_gerais)
#converte os dados para tuplas x,y
X = action.get_x(dados_gerais)
Y = action.get_y(dados_gerais) 
#separa os casos de teste e treino
treino_x, teste_x, treino_y, teste_y =  train_test_split(X.to_numpy(),Y.to_numpy(), test_size= 0.2, random_state=1234) 





#inicializa o objeto KNN
clf = KNN()
#insere os dados de treino
clf.fit(treino_x,treino_y)
#recupera os resultados do teste
previsoes = clf.predict(teste_x) 
#% de acertos do modelo
precisao = (np.sum(previsoes == teste_y)/len(teste_y))*100
precisao = 'Taxa de acertos: '+str(precisao) + '%'
print(precisao)










########################################################
##################PAGINA PRINCIPAL######################
@app.route('/')
def inicio():
    
    return redirect(url_for('home'))

@app.route('/home')
def home():
    
    return render_template(
        'home.html',
        valor_k = 'Valor de K: '+str(clf.k)
    )

@app.route('/alterar_k',methods=['GET','POST'])
def alterar_k():
    try:
        k = request.form['K']
        
        X = clf.k = int (k)
        clf.fit(treino_x,treino_y)
        previsoes = clf.predict(teste_x) 
        precisao = (np.sum(previsoes == teste_y)/len(teste_y))*100
        precisao = 'Taxa de acertos: '+str(precisao) + '%'

        
        flash('Valor de K alterado para: ' + str(clf.k), 'SUCESSO_1')
        return redirect(url_for('home'))
    
    except Exception as e:
        print(e)
        flash('Erro ao formatar o texto', 'ERRO_1')
        return redirect(url_for('home'))

@app.route('/testar_curriculo',methods=['GET','POST'])
def testar_curriculo():
    try:
        exp = request.form['Razão de Experiência']
        pub = request.form['Publicações']
        con = request.form['Conexões']
        
        X = action.concatena_atributos(int(exp),int(pub),int(con))
        X = clf.predict(X)
        
        flash('A qualidade do currículo é: ' + X[0], 'SUCESSO_2')
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
        flash('Erro ao formatar o texto', 'ERRO_2')
        return redirect(url_for('home'))


########################################################
##################PAGINAS DE DADOS######################
@app.route('/dados_treino')
def dados_treino():
    r_dados = action.get_dados(treino_x,treino_y)
    return render_template(
        'dados_treino.html',
        dados = r_dados
    )

@app.route('/dados_teste')
def dados_teste():
    r_dados = action.get_dados_teste(action.get_dados(teste_x, teste_y),previsoes)
    return render_template(
        'dados_teste.html',
        dados = r_dados,
        precisao = precisao
    )



app.run()
