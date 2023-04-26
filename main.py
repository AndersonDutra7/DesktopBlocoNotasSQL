import sys

from PySide6.QtWidgets import QApplication
from controller.bloco_de_notas_dao import DataBase
from view.tela_bloco_de_notas import MainWindow

db = DataBase()
db.connect()
db.create_table_bloco_de_notas()
db.close_connection()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()