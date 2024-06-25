import numpy as np
from collections import Counter

class no:
    def __init__(self, atributo=None, limite=None, esquerda=None, direita=None,*,valor=None):
        self.atributo = atributo
        self.limite = limite
        self.esquerda = esquerda
        self.direita = direita
        self.valor = valor
        
    def e_no_folha(self):
        return self.valor is not None


class AD:
    def __init__(self, divisao_amostras_minimas=2, profundidade_max=100, n_atributos=None):
        self.divisao_amostras_minimas=divisao_amostras_minimas
        self.profundidade_max=profundidade_max
        self.n_atributos=n_atributos
        self.raiz=None

    
    def fit(self, X, y):
        self.n_atributos = X.shape[1] if not self.n_atributos else min(X.shape[1],self.n_atributos)
        self.raiz = self._aumenta_arvore(X, y)

    def _aumenta_arvore(self, X, y, profundidade=0):
        n_amostras, n_atris = X.shape
        n_classes = len(np.unique(y))

        # verifica critério de parada
        if (profundidade>=self.profundidade_max or n_classes==1 or n_amostras<self.divisao_amostras_minimas):
            leaf_valor = self._classe_mais_comum(y)
            return no(valor=leaf_valor)

        atri_idxs = np.random.choice(n_atris, self.n_atributos, replace=False)

        # encontra melhor divisao
        melhor_atributo, melhor_lim = self._melhor_divisao(X, y, atri_idxs)

        # cria nos filhos
        esquerda_idxs, direita_idxs = self._divisao(X[:, melhor_atributo], melhor_lim)
        esquerda = self._aumenta_arvore(X[esquerda_idxs, :], y[esquerda_idxs], profundidade+1)
        direita = self._aumenta_arvore(X[direita_idxs, :], y[direita_idxs], profundidade+1)
        return no(melhor_atributo, melhor_lim, esquerda, direita)


    def _melhor_divisao(self, X, y, atri_idxs):
        melhor_ganho = -1
        divisao_idx, divisao_limite = None, None

        for atri_idx in atri_idxs:
            Coluna_X = X[:, atri_idx]
            limites = np.unique(Coluna_X)

            for thr in limites:
                # calcula ganho informacional
                ganho = self._ganho_informacional(y, Coluna_X, thr)

                if ganho > melhor_ganho:
                    melhor_ganho = ganho
                    divisao_idx = atri_idx
                    divisao_limite = thr

        return divisao_idx, divisao_limite


    def _ganho_informacional(self, y, Coluna_X, limite):
        # entropia do pai
        entropia_pai = self._entropia(y)

        # cria filho
        esquerda_idxs, direita_idxs = self._divisao(Coluna_X, limite)

        if len(esquerda_idxs) == 0 or len(direita_idxs) == 0:
            return 0
        
        # calcula a entropia media do filho
        n = len(y)
        n_l, n_r = len(esquerda_idxs), len(direita_idxs)
        e_l, e_r = self._entropia(y[esquerda_idxs]), self._entropia(y[direita_idxs])
        entropia_filho = (n_l/n) * e_l + (n_r/n) * e_r

        # calcula o ganho 
        information_ganho = entropia_pai - entropia_filho
        return information_ganho

    def _divisao(self, Coluna_X, divisao_lim):
        esquerda_idxs = np.argwhere(Coluna_X <= divisao_lim).flatten()
        direita_idxs = np.argwhere(Coluna_X > divisao_lim).flatten()
        return esquerda_idxs, direita_idxs

    def _entropia(self, y):
        hist = np.bincount(y)
        ps = hist / len(y)
        return -np.sum([p * np.log(p) for p in ps if p>0])


    def _classe_mais_comum(self, y):
        counter = Counter(y)
        valor = counter.most_common(1)[0][0]
        return valor

    def predict(self, X):
        return np.array([self._percorre_arvore(x, self.raiz) for x in X])

    def _percorre_arvore(self, x, no):
        if no.e_no_folha():
            return no.valor

        if x[no.atributo] <= no.limite:
            return self._percorre_arvore(x, no.esquerda)
        return self._percorre_arvore(x, no.direita)