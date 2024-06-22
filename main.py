from flask import Flask, render_template, url_for, flash, request, redirect
from Services import tratamento_de_dados
from user import user

#inicializa o flask
app = Flask(__name__)
app.secret_key = 'Projeto_IA'

#inicializa o objeto de tratamento de dados
action = tratamento_de_dados()

#inicializa o objeto que controla o KNN
controle = user() 





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

@app.route('/testar_curriculo',methods=['GET','POST'])
def testar_curriculo():
    try:
        exp = request.form['Experiência']
        pub = request.form['Publicações']
        con = request.form['Conexões']
        
        X = action.concatena_atributos(int(exp),int(pub),int(con))
        print(X)
        X = controle.clf.predict(X)
        print(X)
        
        flash('A qualidade do currículo é: ' + X[0], 'SUCESSO_1')
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
        flash('Erro ao formatar o texto', 'ERRO_1')
        return redirect(url_for('home'))


########################################################
##################PAGINAS DE DADOS######################
@app.route('/dados_treino')
def dados_treino():
    return render_template(
        'dados_treino.html',
        dados=action.get_dados(controle.treino_x,controle.treino_y)
    )

@app.route('/dados_teste')
def dados_teste():
    return render_template(
        'dados_teste.html',
        dados=action.get_dados(controle.teste_x, controle.teste_y)
    )



app.run()
