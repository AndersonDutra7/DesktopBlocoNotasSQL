import requests
import json
import sys
from datetime import datetime

from PySide6 import QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QLabel, QLineEdit, QWidget, QPushButton,
                               QMessageBox, QSizePolicy, QTableWidget, QAbstractItemView, QTableWidgetItem, QTextEdit)

from infra.configs.connection import DBConnectionHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        conn = DBConnectionHandler()
        conn.create_database()
        self.setMinimumSize(458, 450)

        self.setWindowTitle('BLOCO DE NOTAS')

        self.lbl_id = QLabel('ID')
        self.txt_id = QLineEdit()
        self.txt_id.setMaximumSize(QSize(100, 100))
        self.txt_id.setReadOnly(True)
        self.txt_id.setStyleSheet("background-color: silver;")
        self.lbl_nome_nota = QLabel('TITULO DA NOTA')
        self.txt_nome_nota = QLineEdit()
        self.lbl_nota = QLabel('NOTA')
        self.txt_nota = QTextEdit()
        self.txt_nota.setStyleSheet("background-color: white;")
        self.lbl_notas_cadastradas = QLabel('NOTAS CADASTRADAS')
        self.btn_salvar = QPushButton('Salvar')
        self.btn_salvar.setMaximumSize(QSize(100, 100))
        self.btn_remover = QPushButton('Remover')
        self.btn_remover.setMaximumSize(QSize(100, 100))
        self.btn_limpar = QPushButton('Limpar')
        self.btn_limpar.setMaximumSize(100,100)
        self.tabela_notas_cadastradas = QTableWidget()
        self.tabela_notas_cadastradas.setColumnCount(4)
        self.tabela_notas_cadastradas.setHorizontalHeaderLabels(['ID ', 'NOME_NOTA', 'DATA_NOTA', 'TEXTO_NOTA'])
        self.tabela_notas_cadastradas.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_notas_cadastradas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.txt_data_nota = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_nome_nota)
        layout.addWidget(self.txt_nome_nota)
        layout.addWidget(self.lbl_nota)
        layout.addWidget(self.txt_nota)
        layout.addWidget(self.lbl_notas_cadastradas)
        layout.addWidget(self.tabela_notas_cadastradas)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_remover)
        layout.addWidget(self.btn_limpar)
        self.btn_remover.setVisible(False)
        self.btn_limpar.setVisible(False)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_salvar.clicked.connect(self.salvar_nota)
        self.btn_remover.clicked.connect(self.remover_nota)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.tabela_notas_cadastradas.cellDoubleClicked.connect(self.carregar_dados)
        self.popular_tabela_notas_cadastradas()

    def salvar_nota(self):
        db = DataBase()

        nota = Bloco_De_Notas(
            id = self.txt_id.text(),
            nome_nota = self.txt_nome_nota.text(),
            texto_nota = self.txt_nota.toPlainText(),
            data_nota = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        if self.btn_salvar.text() == 'Salvar':
            if (self.txt_nome_nota.text().split()) and (self.txt_nota.toPlainText().split()):
                retorno = db.criar_nota(nota)
                self.btn_limpar.setVisible(True)
                if retorno == 'Ok':
                    msg = QMessageBox()
                    msg.setWindowTitle('Criação de Nota.')
                    msg.setText('Nota salva com sucesso!')
                    msg.exec()
                elif retorno == 'UNIQUE constraint failed: BLOCO_DE_NOTAS.ID':
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setWindowTitle('Erro ao Criar Nota!')
                    msg.setText(f'O ID {self.txt_id.text()} já existe com o nome {self.txt_nome_nota.text()}')
                    msg.exec()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao Criar Nota!')
                msg.setText('Os campos devem ser preenchidos ...')
                msg.exec()
        elif self.btn_salvar.text() == 'Atualizar':
            retorno = db.editar_nota(nota)
            if retorno == 'Ok':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Edição de Nota')
                msg.setText('Nota atualizada.')
                msg.exec()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao Atualizar Nota! ')
                msg.setText('Alguma coisa não esta certa!\nPor favor, tente novamente!')
                msg.exec()
        self.popular_tabela_notas_cadastradas()
        self.btn_limpar.setVisible(False)
        self.limpar_campos()

    def consultar_nota(self):
        if self.txt_id.text() != '':
            db = DataBase()
            retorno = db.consulta_todas_notas(self.txt_id.text())

            if retorno is not None:
                self.btn_salvar.setText('Atualizar')
                msg = QMessageBox()
                msg.setWindowTitle('Nota já Salva.')
                msg.setText(f'A nota {self.txt_id.text()} já esta salva')
                msg.exec()
                self.txt_nome_nota.setText(retorno[1])
                self.txt_nota.setText(retorno[2])
                self.txt_data_nota.setText(retorno[3])
                self.btn_remover.setVisible(True)

    def remover_nota(self):
        db = DataBase()
        msg = QMessageBox()
        msg.setWindowTitle('Remover Nota')
        msg.setText('Confirma a exclusão abaixo?!')
        msg.setInformativeText(f'\nNOTA: {self.txt_id.text()} \nNOME: {self.txt_nome_nota.text()} ?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')

        resposta = msg.exec()

        if resposta == QMessageBox.Yes:
            retorno = db.excluir_nota(self.txt_id.text())
            if retorno == 'Ok':
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover Nota')
                nv_msg.setText('Nota removida com sucesso!')
                nv_msg.exec()
                self.limpar_campos()
            else:
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover Nota')
                nv_msg.setText(f'Erro ao remover nota.')
                nv_msg.exec()
        elif resposta == QMessageBox.No:
            self.limpar_campos()
        self.popular_tabela_notas_cadastradas()
        self.txt_nome_nota.setReadOnly(False)
        self.btn_limpar.setVisible(False)

    def limpar_campos(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QTextEdit):
                widget.clear()
        self.btn_salvar.setText('Salvar')
        self.txt_id.setStyleSheet("background-color: silver;")
        self.btn_remover.setVisible(False)
        self.btn_limpar.setVisible(False)

    def popular_tabela_notas_cadastradas(self):
        self.tabela_notas_cadastradas.setRowCount(0)
        db = DataBase()
        lista_notas = db.consulta_todas_notas()
        self.tabela_notas_cadastradas.setRowCount(len(lista_notas))

        for linha, nota in enumerate(lista_notas):
            for coluna, valor in enumerate(nota):
                self.tabela_notas_cadastradas.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    def carregar_dados(self, row, column):
        self.txt_id.setStyleSheet("background-color: white;")
        self.txt_id.setText(self.tabela_notas_cadastradas.item(row, 0).text())
        self.txt_nome_nota.setText(self.tabela_notas_cadastradas.item(row, 1).text())
        self.txt_data_nota.setText(self.tabela_notas_cadastradas.item(row, 2).text())
        self.txt_nota.setText(self.tabela_notas_cadastradas.item(row, 3).text())
        self.btn_salvar.setText('Atualizar')
        self.btn_remover.setVisible(True)
        self.btn_limpar.setVisible(True)
        self.txt_id.setReadOnly(True)