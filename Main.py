import sys

from Logic import Field

from PyQt5.QtWidgets import QWidget, QApplication
from Graphics import Scene
numV, numP, numW = 10,8,6
field = Field(numV, numP, numW)

if __name__ == '__main__':
    app = QApplication([])
    scene = Scene(field)
    sys.exit(app.exec_())
