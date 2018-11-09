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
        self.botaoArvore =QPushButton("Vizualizar Arvore de Decisoes",self)
        self.botaoArvore.clicked.connect(self.gerar_arvore)
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
        self.main_layout.addRow(self.botaoArvore)

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
        novo_action.triggered.connect(self.gerar_arvore)

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
        subprocess.run([imageViewerFromCommandLine, '/home/lyncon/Desktop/Trab top/tree2.png'])


class JanelaNovo(QDialog):
    def __init__(self):
        super(JanelaNovo,self).__init__()
        self.resize(550, 200)
        self.setWindowTitle("Configurations")
        self.setMinimumWidth(350)
        self.setWindowIcon(QIcon("../Icons/config.png"))
        self.center()

        title_font = QFont("Times", 20, QFont.Bold)
        lb_title = QLabel("Configurations", self)
        lb_title.setFont(title_font)
        lb_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lb_title.setAlignment(Qt.AlignCenter)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.ply = QLineEdit()
        self.ply.setText(ply_default)
        self.output = QLineEdit()
        self.output.setText(output_default)
        self.image = QLineEdit()
        self.image.setText(image_dir_default)
        self.texture = QLineEdit()
        self.texture.setText(texture_file)
        self.ply_button = QPushButton("Browse", self)
        self.ply_button.clicked.connect(self.browse_ply)
        self.obj_button = QPushButton("Browse", self)
        self.obj_button.clicked.connect(self.browse_obj)
        self.image_button = QPushButton("Browse", self)
        self.image_button.clicked.connect(self.browse_image_dir)
        self.texture_button = QPushButton("Browse", self)
        self.texture_button.clicked.connect(self.browse_texture_file)

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox1.addWidget(self.ply)
        hbox1.addWidget(self.ply_button)
        hbox2.addWidget(self.output)
        hbox2.addWidget(self.obj_button)
        hbox3.addWidget(self.image)
        hbox3.addWidget(self.image_button)
        hbox4.addWidget(self.texture)
        hbox4.addWidget(self.texture_button)
        layout = QFormLayout()
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        layout.addRow(lb_title)
        layout.addRow("<b>Path to save Ply File</b>", hbox1)
        layout.addRow("<b>Path to save OBJ file</b>", hbox2)
        layout.addRow("<b>Directory to save layer Images</b>", hbox3)
        layout.addRow("<b>Path to save OBJ file with texture</b>", hbox4)
        layout.addWidget(self.button_box)
        layout.setSpacing(20)

        self.setLayout(layout)

App = QApplication(sys.argv)
window = JanelaPrincipal()
window.show()
sys.exit(App.exec())