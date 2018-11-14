from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from back import *
import pydot
import subprocess

class JanelaPrincipal(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adivinhator 2000")
        self.resize(680,500)
     
        self.fonte_titulo = QFont("Times", 20, QFont.Bold)

        self.func = Funcoes()
        p = self.palette()
        p.setColor(self.backgroundRole(),Qt.darkBlue)
        self.setPalette(p)

        self.main_layout = QFormLayout()
        self.main_layout.setSpacing(20)

        self.titulo = QLabel("Preencha os Campos com Informações de um Campeão de League of Legends", self)
        self.titulo.setFont(self.fonte_titulo)
        self.titulo.setAlignment(Qt.AlignCenter)

        self.input_cor = QLineEdit()
        self.input_corCabelo = QLineEdit()
        self.input_humano = QLineEdit()
        self.input_lane = QLineEdit()
        self.input_lugarOrigem = QLineEdit()
        self.input_arma = QLineEdit() 
        self.botaoArvore =QPushButton("Vizualizar Arvore de Decisoes",self)
        self.botaoArvore.clicked.connect(self.gerar_arvore)
        self.botao = QPushButton("Adivinhar!!",self)
        self.botao.clicked.connect(self.advinhar)

        self.main_layout.addRow(self.titulo)
        self.main_layout.addRow(QLabel("cor: "),self.input_cor)
        self.main_layout.addRow(QLabel("Cor do Cabelo: "), self.input_corCabelo)
        self.main_layout.addRow(QLabel("È humano? "), self.input_humano)
        self.main_layout.addRow(QLabel("Posicao em que joga: "), self.input_lane)
        self.main_layout.addRow(QLabel("lugar de Origem: "), self.input_lugarOrigem)
        self.main_layout.addRow(QLabel("Arma que utiliza: "), self.input_arma)
        self.main_layout.addRow(self.botao)
        self.main_layout.addRow(self.botaoArvore)

        self.setLayout(self.main_layout)

    def advinhar(self):
        chute = [self.input_cor.text(),self.input_corCabelo.text(),self.input_humano.text(),self.input_lane.text(),self.input_lugarOrigem.text(),self.input_arma.text()]
        if (self.func.valida_personagem(chute)):
            chute_codificado = self.func.codificar_resposta(chute)
            personagem = self.func.gerar_predict(chute_codificado)

            personagem =''.join(map(str, personagem))
            print(personagem)

            msg = QMessageBox()
            pixmap = QPixmap("Imagens/"+personagem+".jpg")
            pixmap.scaled(64,64,Qt.KeepAspectRatio)
            msg.setIconPixmap(pixmap)

            msg.setText("Seu Personagem é: "+personagem)
            msg.setWindowTitle("Personagem Encontrado")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        else:
            nomeNovo, okPressionado = QInputDialog.getText(self, "Personagem Não Encontrado", "Personagem nao Encontrado! \nDigite seu nome para ser adicionado a base de dados:", QLineEdit.Normal, "")
            if okPressionado and nomeNovo != '':
                self.func.acrescenta_dados(chute)
                self.func.novo_personagem(nomeNovo, chute)
                QMessageBox.information(self,"Inserido","Personagem Inserido com Sucesso",QMessageBox.Ok,QMessageBox.Ok)
            elif okPressionado:
                QMessageBox.warning(self, "Erro", "Personagem não Inserido devido à um erro", QMessageBox.Ok,QMessageBox.Ok)

    def gerar_arvore(self):

        export_graphviz(self.func.arvore, out_file='tree.dot', class_names=self.func.data_set_num["campeao"],
                       feature_names=['cor', 'CorCabelo', 'humano', 'lane', 'lugarOrigem','arma'], impurity=False,
                        filled=True)

        (graph,) = pydot.graph_from_dot_file('tree.dot')
        graph.write_png('tree2.png')
        imageViewerFromCommandLine = {'linux': 'eog',
                                      'win32': 'explorer',
                                      'darwin': 'open'}[sys.platform]
        subprocess.run([imageViewerFromCommandLine, '/home/lyncon/AkinatorPython/tree2.png'])

App = QApplication(sys.argv)
window = JanelaPrincipal()
window.show()
sys.exit(App.exec())