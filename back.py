# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import export_graphviz
from shutil import copyfile

class Funcoes:
    def __init__(self):
        copyfile("simp.csv", "simpCopia.csv")

        #-------------------------Criando Caracteristicas----------------------------
        self.sexos = ["Masculino","Feminino"]
        self.cores_cabelos = ["Preto","Cinza","Vermelho","Amarelo","Azul","Careca","CastanhoClaro","CastanhoEscuro","Cinza","Branco","Verde"]
        self.compr_cabelos = ["Curto","Medio","Longo","Careca"]
        self.tipos_cabelos = ["Fios","Triangulos","Liso","Crespo","Careca"]
        self.idades = ["Bebê","Criança","Adulto","Velho"]
        self.cores_roupas = ["Laranja","Branco","Verde","Marrom","Azul","Vermelho","Preto","Amarelo","Azul","Roxo","Cinza","Sem Roupa"]
        self.oculos = ["Nao","Sim"]
        self.cores_pele = ["Amarelo","Marrom"]
        self.cores_sapatos = ["Preto","Cinza","Laranja","Vermelho","Roxo","Marrom","Verde","Azul","Rosa","Sem Sapato"]

        #-------------------------Criando label Encoders-------------------------------
        self.encoder_sexo = LabelEncoder()
        self.encoder_corCabelo = LabelEncoder()
        self.encoder_comprCabelo = LabelEncoder()
        self.encoder_tipoCabelo = LabelEncoder()
        self.encoder_idade = LabelEncoder()
        self.encoder_corRoupa = LabelEncoder()
        self.encoder_oculos = LabelEncoder()
        self.encoder_corPele = LabelEncoder()
        self.encoder_corSapato = LabelEncoder()

        self.arvore = DecisionTreeClassifier(criterion="gini")

        self.encode_dados()

    def acrescenta_dados(self,advinha):#Funcao para Acrescentar dados que nao existiam no Label Encoder
        for i in range(len(advinha)):
            if i == 0:
                if not any(advinha[i] in s for s in self.sexos):
                    self.sexos.append(advinha[i])
                    print("oi")
            if i == 1:
                if not any(advinha[i] in s for s in self.cores_cabelos):
                    self.cores_cabelos.append(advinha[i])
            if i == 2:
                if not any(advinha[i] in s for s in self.compr_cabelos):
                    self.compr_cabelos.append(advinha[i])
            if i == 3:
                if not any(advinha[i] in s for s in self.tipos_cabelos):
                    self.tipos_cabelos.append(advinha[i])
            if i == 4:
                if not any(advinha[i] in s for s in self.idades):
                    self.idades.append(advinha[i])
            if i == 5:
                if not any(advinha[i] in s for s in self.cores_roupas):
                    self.cores_roupas.append(advinha[i])
            if i == 6:
                if not any(advinha[i] in s for s in self.oculos):
                    self.oculos.append(advinha[i])
            if i == 7:
                if not any(advinha[i] in s for s in self.cores_pele):
                    self.cores_pele.append(advinha[i])
            if i == 8:
                if not any(advinha[i] in s for s in self.cores_sapatos):
                    self.cores_sapatos.append(advinha[i])


    def novo_personagem(self,nome,advinha):         # Funcao para Escrever novo personagem no Arquivo CSV
        with open("simpCopia.csv","a") as arquivo:
            linha = ",".join(advinha)
            linha = "\n"+nome+","+linha
            arquivo.write(linha)
        self.encode_dados()

    def encode_dados(self):                         # Funcao para preencher DataFrame com Dados Numericos e Dados Categoricos
        self.data_set_categorica = pd.read_csv('simpCopia.csv', sep=',', header=0)
        self.data_set_num = pd.read_csv('simpCopia.csv', sep=',', header=0)
        self.encoder_sexo.fit(self.sexos)
        self.data_set_num["Sexo"] = self.encoder_sexo.fit_transform(self.data_set_num["Sexo"])
        self.encoder_corCabelo.fit(self.cores_cabelos)
        self.data_set_num["CorCabelo"] = self.encoder_corCabelo.fit_transform(self.data_set_num["CorCabelo"])
        self.encoder_comprCabelo.fit(self.compr_cabelos)
        self.data_set_num["ComprCabelo"] = self.encoder_comprCabelo.fit_transform(self.data_set_num["ComprCabelo"])
        self.encoder_tipoCabelo.fit(self.tipos_cabelos)
        self.data_set_num["TipoCabelo"] = self.encoder_tipoCabelo.fit_transform(self.data_set_num["TipoCabelo"])
        self.encoder_idade.fit(self.idades)
        self.data_set_num["Idade"] = self.encoder_idade.fit_transform(self.data_set_num["Idade"])
        self.encoder_corRoupa.fit(self.cores_roupas)
        self.data_set_num["CorRoupa"] = self.encoder_corRoupa.fit_transform(self.data_set_num["CorRoupa"])
        self.encoder_oculos.fit(self.oculos)
        self.data_set_num["Oculos"] = self.encoder_oculos.fit_transform(self.data_set_num["Oculos"])
        self.encoder_corPele.fit(self.cores_pele)
        self.data_set_num["CorPele"] = self.encoder_corPele.fit_transform(self.data_set_num["CorPele"])
        self.encoder_corSapato.fit(self.cores_sapatos)
        self.data_set_num["CorSapato"] = self.encoder_corSapato.fit_transform(self.data_set_num["CorSapato"])

        self.arvore.fit(self.data_set_num[["Sexo", "CorCabelo", "ComprCabelo", "TipoCabelo", "Idade", "CorRoupa", "Oculos", "CorPele","CorSapato"]], self.data_set_num["Nome"])


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
            if cont == 9:
                achou = True
                break
        return achou

    def gerar_predict(self,chute):

        self.arvore.fit(self.data_set_num[["Sexo","CorCabelo","ComprCabelo","TipoCabelo","Idade","CorRoupa","Oculos","CorPele","CorSapato"]], self.data_set_num["Nome"])

        previsao = self.arvore.predict([chute])

        return previsao
        
    def codificar_resposta(self,chute):             # Funcao para transformar chute Categorico em Numerico
        chute[0]=self.encoder_sexo.transform([chute[0]])
        chute[0]=''.join(map(str, chute[0]))

        chute[1]=self.encoder_corCabelo.transform([chute[1]])
        chute[1]=''.join(map(str, chute[1]))

        chute[2]=self.encoder_comprCabelo.transform([chute[2]])
        chute[2]=''.join(map(str, chute[2]))

        chute[3]=self.encoder_tipoCabelo.transform([chute[3]])
        chute[3]=''.join(map(str, chute[3]))

        chute[4]=self.encoder_idade.transform([chute[4]])
        chute[4]=''.join(map(str, chute[4]))

        chute[5]=self.encoder_corRoupa.transform([chute[5]])
        chute[5]=''.join(map(str, chute[5]))

        chute[6]=self.encoder_oculos.transform([chute[6]])
        chute[6]=''.join(map(str, chute[6]))

        chute[7]=self.encoder_corPele.transform([chute[7]])
        chute[7]=''.join(map(str, chute[7]))

        chute[8]=self.encoder_corSapato.transform([chute[8]])
        chute[8]=''.join(map(str, chute[8]))

        return chute


if "__main__" == __name__:
    trat = Funcoes()
    chute = ["Masculino","Cinza","Gigante","Crespo","Velho","Azul","Nao","Amarelo","Preto"]
    for i in range(2):
        if(trat.valida_personagem(chute)):
            chute_codificado = trat.codificar_resposta(chute)
            prs=trat.gerar_predict(chute_codificado)
            print(prs)
        else:
            trat.acrescenta_dados(chute)
            trat.novo_personagem("Caralho",chute)
            print(trat.data_set_num)
            print("inserido")