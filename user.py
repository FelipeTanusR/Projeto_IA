from Services import tratamento_de_dados
from sklearn.model_selection import train_test_split
from KNN import KNN
action = tratamento_de_dados()

class user:
    def __init__(self):
        #busca os dados do arquivo excel
        self.dados_gerais = action.get_dados_gerais()

        #converte os dados para tuplas x,y
        self.X = action.get_x(self.dados_gerais)
        self.Y = action.get_y(self.dados_gerais) 

        #separa os casos de teste e treino
        self.treino_x, self.teste_x, self.treino_y, self.teste_y =  train_test_split(self.X.to_numpy(),self.Y.to_numpy(), test_size= 0.2, random_state=1234) 

        #inicializa o objeto KNN
        self.clf = KNN()
        
        #insere os dados de treino
        self.clf.fit(self.treino_x,self.treino_y)

        #recupera os resultados do teste
        self.teste_y = self.clf.predict(self.teste_x)

