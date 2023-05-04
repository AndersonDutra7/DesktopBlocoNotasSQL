import sys

from PySide6.QtWidgets import QApplication
from view.tela_bloco_de_notas import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
