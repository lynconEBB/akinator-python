# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import export_graphviz
from shutil import copyfile

class Funcoes:
    def __init__(self):
        copyfile("personagens_caracteristicas.csv", "lolCopia.csv")

        #-------------------------Criando Caracteristicas----------------------------
        self.cores = ["verde","roxa","branco","cinza","preto","azul","moreno","negro","laranja","amarelo"]
        self.cores_cabelos = ["verde","castanho","loiro","branco","careca","nao tem","preto","azul","vermelho","laranja","roxo"]
        self.humano = ["sim","nao"]
        self.lanes = ["adcarry","suporte","jungle","top","mid"]
        self.lugaresOrigem = ["demacia","zaun","bandopolis","shurima","targon","ionia","freljord","aguas de sentina","ilha das sombras","piltover","vazio","noxus"]
        self.armas = ["garras","cajado","espada","machado","martelo","magia","tentaculos","laminas","lança","chakram","shurikens","arco e flecha","arma de fogo","arma viva","foice","adaga","besta","boomerang","kamas","faixas"]

        #-------------------------Criando label Encoders-------------------------------
        self.encoder_cor = LabelEncoder()
        self.encoder_corCabelo = LabelEncoder()
        self.encoder_humano = LabelEncoder()
        self.encoder_lane = LabelEncoder()
        self.encoder_lugarOrigem = LabelEncoder()
        self.encoder_arma = LabelEncoder()

        self.encode_dados()

    def acrescenta_dados(self,advinha):#Funcao para Acrescentar dados que nao existiam no Label Encoder
        for i in range(len(advinha)):
            if i == 0:
                if not any(advinha[i] in s for s in self.cores):
                    self.cores.append(advinha[i])
            if i == 1:
                if not any(advinha[i] in s for s in self.cores_cabelos):
                    self.cores_cabelos.append(advinha[i])
            if i == 2:
                if not any(advinha[i] in s for s in self.humano):
                    self.humano.append(advinha[i])
            if i == 3:
                if not any(advinha[i] in s for s in self.lanes):
                    self.lanes.append(advinha[i])
            if i == 4:
                if not any(advinha[i] in s for s in self.lugaresOrigem):
                    self.lugaresOrigem.append(advinha[i])
            if i == 5:
                if not any(advinha[i] in s for s in self.armas):
                    self.armas.append(advinha[i])


    def novo_personagem(self,nome,advinha):         # Funcao para Escrever novo personagem no Arquivo CSV
        with open("lolCopia.csv","a") as arquivo:
            linha = ",".join(advinha)
            linha = "\n"+nome+","+linha
            arquivo.write(linha)
        self.encode_dados()

    def encode_dados(self):                         # Funcao para preencher DataFrame com Dados Numericos e Dados Categoricos
        self.data_set_categorica = pd.read_csv('lolCopia.csv', sep=',', header=0)
        self.data_set_num = pd.read_csv('lolCopia.csv', sep=',', header=0)
        self.encoder_cor.fit(self.cores)
        self.data_set_num["cor"] = self.encoder_cor.fit_transform(self.data_set_num["cor"])
        self.encoder_corCabelo.fit(self.cores_cabelos)
        self.data_set_num["corCabelo"] = self.encoder_corCabelo.fit_transform(self.data_set_num["corCabelo"])
        self.encoder_humano.fit(self.humano)
        self.data_set_num["humano"] = self.encoder_humano.fit_transform(self.data_set_num["humano"])
        self.encoder_lane.fit(self.lanes)
        self.data_set_num["lane"] = self.encoder_lane.fit_transform(self.data_set_num["lane"])
        self.encoder_lugarOrigem.fit(self.lugaresOrigem)
        self.data_set_num["lugarOrigem"] = self.encoder_lugarOrigem.fit_transform(self.data_set_num["lugarOrigem"])
        self.encoder_arma.fit(self.armas)
        self.data_set_num["arma"] = self.encoder_arma.fit_transform(self.data_set_num["arma"])

    def valida_personagem(self,advinha):                #Funcao para verificar se personagem pesquisado existe no dataFrame
        achou = False
        lista_personagens = self.data_set_categorica.values.tolist()
        for personagem in lista_personagens:
            i=-1
            cont = 0
            mudancas = []

            for atributo in personagem:
                if i > -1:
                    if atributo == advinha[i]:
                        cont+=1
                        mudancas.append(True)
                    else:
                        mudancas.append(False)
                i+=1
            if cont == 6:
                achou = True
                break
        return achou

    def gerar_predict(self,chute):
        self.arvore = DecisionTreeClassifier(criterion="entropy")
        self.arvore.fit(self.data_set_num[["cor","corCabelo","humano","lane","lugarOrigem","arma"]], self.data_set_num["campeao"])

        previsao = self.arvore.predict([chute])

        return previsao
        
    def codificar_resposta(self,chute):             # Funcao para transformar chute Categorico em Numerico
        chute[0]=self.encoder_cor.transform([chute[0]])
        chute[0]=''.join(map(str, chute[0]))

        chute[1]=self.encoder_corCabelo.transform([chute[1]])
        chute[1]=''.join(map(str, chute[1]))

        chute[2]=self.encoder_humano.transform([chute[2]])
        chute[2]=''.join(map(str, chute[2]))

        chute[3]=self.encoder_lane.transform([chute[3]])
        chute[3]=''.join(map(str, chute[3]))

        chute[4]=self.encoder_lugarOrigem.transform([chute[4]])
        chute[4]=''.join(map(str, chute[4]))

        chute[5]=self.encoder_arma.transform([chute[5]])
        chute[5]=''.join(map(str, chute[5]))

        return chute


if "__main__" == __name__:
    trat = Funcoes()
    chute = ["negro","castanho","sim","adcarry","demacia","arma de fogo"]
    if(trat.valida_personagem(chute)):
        chute_codificado = trat.codificar_resposta(chute)
        prs=trat.gerar_predict(chute_codificado)
        print(prs)
    else:
        trat.acrescenta_dados(chute)
        trat.novo_personagem("Caralho",chute)
        print(trat.data_set_num)
        print("inserido")