from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from back import *
import pydot
import subprocess

class JanelaPrincipal(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Jogo de Adivinhacao")
        self.resize(680,500)
     
        self.fonte_titulo = QFont("Times", 20, QFont.Bold)

        self.func = Funcoes()
        p = self.palette()
        p.setColor(self.backgroundRole(),Qt.yellow)
        self.setPalette(p)

        self.main_layout = QFormLayout()
        self.main_layout.setSpacing(20)

        self.titulo = QLabel("Preencha os Campos com Informações de um personagem dos Simpsons", self)
        self.titulo.setFont(self.fonte_titulo)
        self.titulo.setAlignment(Qt.AlignCenter)

        self.input_sexo = QLineEdit()
        self.input_corCabelo = QLineEdit()
        self.input_comprCabelo = QLineEdit()
        self.input_tipoCabelo = QLineEdit()
        self.input_idade = QLineEdit()
        self.input_corRoupa = QLineEdit()
        self.input_oculos = QLineEdit()
        self.input_corPele = QLineEdit()
        self.input_corSapato = QLineEdit()
        self.botaoArvore =QPushButton("Vizualizar Arvore de Decisoes",self)
        self.botaoArvore.clicked.connect(self.gerar_arvore)
        self.botao = QPushButton("Adivinhar!!",self)
        self.botao.clicked.connect(self.advinhar)

        self.main_layout.addRow(self.titulo)
        self.main_layout.addRow(QLabel("Sexo: "),self.input_sexo)
        self.main_layout.addRow(QLabel("Cor do Cabelo: "), self.input_corCabelo)
        self.main_layout.addRow(QLabel("Comprimento do Cabelo: "), self.input_comprCabelo)
        self.main_layout.addRow(QLabel("Tipo Cabelo: "), self.input_tipoCabelo)
        self.main_layout.addRow(QLabel("Idade: "), self.input_idade)
        self.main_layout.addRow(QLabel("Cor da Roupa(Camisa ou Vestido): "), self.input_corRoupa)
        self.main_layout.addRow(QLabel("Usa Oculos? "), self.input_oculos)
        self.main_layout.addRow(QLabel("Cor da Pele: "), self.input_corPele)
        self.main_layout.addRow(QLabel("Cor do Sapato: "), self.input_corSapato)
        self.main_layout.addRow(self.botao)
        self.main_layout.addRow(self.botaoArvore)

        self.setLayout(self.main_layout)



    def advinhar(self):
        chute = [self.input_sexo.text(),self.input_corCabelo.text(),self.input_comprCabelo.text(),self.input_tipoCabelo.text(),self.input_idade.text(),self.input_corRoupa.text(),
                 self.input_oculos.text(),self.input_corPele.text(),self.input_corSapato.text()] 
        if (self.func.valida_personagem(chute)):
            chute_codificado = self.func.codificar_resposta(chute)
            personagem = self.func.gerar_predict(chute_codificado)

            personagem =''.join(map(str, personagem))
            print(personagem)

            msg = QMessageBox()
            msg.setIconPixmap(QPixmap("Imagens/"+personagem+".png"))

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

        export_graphviz(self.func.arvore, out_file='tree.dot', class_names=self.func.data_set_num["Nome"],
                       feature_names=['Sexo', 'CorCabelo', 'ComprCabelo', 'TipoCabelo', 'Idade','CorRoupa','Oculos','CorPele','CorSapato'], impurity=False,
                        filled=True)

        (graph,) = pydot.graph_from_dot_file('tree.dot')
        graph.write_png('tree2.png')
        imageViewerFromCommandLine = {'linux': 'eog',
                                      'win32': 'explorer',
                                      'darwin': 'open'}[sys.platform]
        subprocess.run([imageViewerFromCommandLine, '/home/lyncon/Desktop/Trab top/tree2.png'])




App = QApplication(sys.argv)
window = JanelaPrincipal()
window.show()
sys.exit(App.exec())