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

        p2 = self.palette()
        p2.setColor(self.backgroundRole(), Qt.green)

        self.setPalette(p)

        self.main_layout = QFormLayout()
        self.main_layout.setSpacing(20)

        self.titulo = QLabel("Preencha os Campos com Informações\nde um personagem dos Simpsons", self)

        self.titulo.setFont(self.fonte_titulo)
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setAutoFillBackground(True)
        self.titulo.setPalette(p2)

        self.init_ui()

        self.win = QWidget()
        self.win.setLayout(self.main_layout)
        self.setCentralWidget(self.win)

        tool_bar = QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea, tool_bar)
        tool_bar.setIconSize(QSize(40, 40))

        arvore_action = QAction(QIcon("Imagens/iconeArvore.png"), "Arvore de Decisão", self)
        arvore_action.setStatusTip("Gera e visualiza arvore de decisão")
        tool_bar.addAction(arvore_action)
        arvore_action.triggered.connect(self.gerar_arvore)

        novo_action = QAction(QIcon("Imagens/novo.png"), "Novo Personagem", self)
        novo_action.setStatusTip("Inserir novo personagem na base de dados")
        tool_bar.addAction(novo_action)
        novo_action.triggered.connect(self.inserir_pers)

    def init_ui(self):
        self.combo_sexo = QComboBox()
        self.combo_sexo.addItems(self.func.sexos)
        self.combo_corCabelo = QComboBox()
        self.combo_corCabelo.addItems(self.func.cores_cabelos)
        self.combo_comprCabelo = QComboBox()
        self.combo_comprCabelo.addItems(self.func.compr_cabelos)
        self.combo_tipoCabelo = QComboBox()
        self.combo_tipoCabelo.addItems(self.func.tipos_cabelos)
        self.combo_idade = QComboBox()
        self.combo_idade.addItems(self.func.idades)
        self.combo_corRoupa = QComboBox()
        self.combo_corRoupa.addItems(self.func.cores_roupas)
        self.combo_oculos = QComboBox()
        self.combo_oculos.addItems(self.func.oculos)
        self.combo_corPele = QComboBox()
        self.combo_corPele.addItems(self.func.cores_pele)
        self.combo_corSapato = QComboBox()
        self.combo_corSapato.addItems(self.func.cores_sapatos)
        self.botao = QPushButton("Adivinhar!!",self)
        self.botao.clicked.connect(self.advinhar)

        self.main_layout.addRow(self.titulo)
        self.main_layout.addRow(QLabel("Sexo: "),self.combo_sexo)
        self.main_layout.addRow(QLabel("Cor do Cabelo: "), self.combo_corCabelo)
        self.main_layout.addRow(QLabel("Comprimento do Cabelo: "), self.combo_comprCabelo)
        self.main_layout.addRow(QLabel("Tipo Cabelo: "), self.combo_tipoCabelo)
        self.main_layout.addRow(QLabel("Idade: "), self.combo_idade)
        self.main_layout.addRow(QLabel("Cor da Roupa(Camisa ou Vestido): "), self.combo_corRoupa)
        self.main_layout.addRow(QLabel("Usa Oculos? "), self.combo_oculos)
        self.main_layout.addRow(QLabel("Cor da Pele: "), self.combo_corPele)
        self.main_layout.addRow(QLabel("Cor do Sapato: "), self.combo_corSapato)
        self.main_layout.addRow(self.botao)

    def update_combo(self):
        self.combo_sexo.clear()
        self.combo_corCabelo.clear()
        self.combo_comprCabelo.clear()
        self.combo_tipoCabelo.clear()
        self.combo_idade.clear()
        self.combo_corRoupa.clear()
        self.combo_oculos.clear()
        self.combo_corPele.clear()
        self.combo_corSapato.clear()
        self.combo_sexo.addItems(self.func.sexos)
        self.combo_corCabelo.addItems(self.func.cores_cabelos)
        self.combo_comprCabelo.addItems(self.func.compr_cabelos)
        self.combo_tipoCabelo.addItems(self.func.tipos_cabelos)
        self.combo_idade.addItems(self.func.idades)
        self.combo_corRoupa.addItems(self.func.cores_roupas)
        self.combo_oculos.addItems(self.func.oculos)
        self.combo_corPele.addItems(self.func.cores_pele)
        self.combo_corSapato.addItems(self.func.cores_sapatos)

    def advinhar(self):
        chute = [self.combo_sexo.currentText(),self.combo_corCabelo.currentText(),self.combo_comprCabelo.currentText(),self.combo_tipoCabelo.currentText(),self.combo_idade.currentText(),self.combo_corRoupa.currentText(),
                 self.combo_oculos.currentText(),self.combo_corPele.currentText(),self.combo_corSapato.currentText()] 
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
        subprocess.run([imageViewerFromCommandLine, '/home/lyncon/AkinatorPython/tree2.png'])

    def inserir_pers(self):
        add_janela = JanelaNovo()
        if add_janela.exec_():
            per = [add_janela.input_sexo.text(),add_janela.input_corCabelo.text(),add_janela.input_comprCabelo.text(),add_janela.input_tipoCabelo.text(),add_janela.input_idade.text(),add_janela.input_corRoupa.text(),
                   add_janela.input_oculos.text(),add_janela.input_corPele.text(),add_janela.input_corSapato.text()]
            self.func.acrescenta_dados(per)
            self.func.novo_personagem(str(add_janela.input_nome.text()), per)
            QMessageBox.information(self, "Inserido", "Personagem Inserido com Sucesso", QMessageBox.Ok, QMessageBox.Ok)
            self.update_combo()


class JanelaNovo(QDialog):
    def __init__(self):
        super(JanelaNovo,self).__init__()
        self.resize(550, 200)
        self.setWindowTitle("Adicionar Personagem")
        self.setMinimumWidth(350)
        self.setWindowIcon(QIcon("../Icons/config.png"))

        title_font = QFont("Times", 20, QFont.Bold)
        lb_title = QLabel("Adicionar Personagem", self)
        lb_title.setFont(title_font)
        lb_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lb_title.setAlignment(Qt.AlignCenter)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.input_nome = QLineEdit()
        self.input_sexo = QLineEdit()
        self.input_corCabelo = QLineEdit()
        self.input_comprCabelo = QLineEdit()
        self.input_tipoCabelo = QLineEdit()
        self.input_idade = QLineEdit()
        self.input_corRoupa = QLineEdit()
        self.input_oculos = QLineEdit()
        self.input_corPele = QLineEdit()
        self.input_corSapato = QLineEdit()

        layout = QFormLayout()
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        layout.addRow(lb_title)
        layout.addRow("<b>Nome: </b>", self.input_nome)
        layout.addRow("<b>Sexo: </b>", self.input_sexo)
        layout.addRow("<b>Cor do Cabelo: </b>", self.input_corCabelo)
        layout.addRow("<b>Comprimento do Cabelo: </b>", self.input_comprCabelo)
        layout.addRow("<b>Tipo de Cabelo: </b>", self.input_tipoCabelo)
        layout.addRow("<b>Idade: </b>", self.input_idade)
        layout.addRow("<b>Cor da Roupa: </b>", self.input_corRoupa)
        layout.addRow("<b>Usa Oculos? </b>", self.input_oculos)
        layout.addRow("<b>Cor da Pele</b>", self.input_corPele)
        layout.addRow("<b>Cor do Sapato</b>", self.input_corSapato)

        layout.addWidget(self.button_box)
        layout.setSpacing(20)

        self.setLayout(layout)

App = QApplication(sys.argv)
window = JanelaPrincipal()
window.show()
sys.exit(App.exec())