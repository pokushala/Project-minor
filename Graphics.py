import sys
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QSlider, QPushButton, QLabel, QLCDNumber #,QGridLayout,QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QColor, QBrush, QPixmap, QPainter
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal


#все поле
class Board(QFrame):
    msgStatBar = pyqtSignal(str)
#параметры поля
    BoardWidth = 15
    BoardHeight = 15
    BoardSpeed = 500

    def __init__(self, parent):
        super().__init__(parent)
        self.field = parent.field
        self.initBoard()

    def initBoard(self):

        self.timer = QBasicTimer()
        self.x = 0
        self.y = 0
        self.setFocusPolicy(Qt.StrongFocus)
        self.isStart = False
        self.isPaused = False

    #def start(self):
    #    if self.isPaused:
    #        return
    #    self.isStart=True
    #    self.timer.start(Board.BoardSpeed, self)

    #def# pause(self):
    #    if not self.isStart:
    #        return
    #    self.isPaused = not self.isPaused

    #    if self.isPaused:
    #        self.timer.stop()
    #    else:
    #        self.timer.start(Board.BoardSpeed, self)
    #    self.update()

    #def kewPressEvent(self, event):
    #    if not self.isStarted:
    #        super(Board,self).keyPressEvent(event)
    #        return
    #    key=event.key()
    #    if key==Qt.Key_Space:#
    #        self.pause()
    #       return
    #    else:
    #        super(Board, self).keyPressEvent(event)



    def start(self):
        if self.isPaused:
            return

        self.msgStatBar.emit(str('started'))
        self.timer.start(Board.BoardSpeed, self)

    def timerEvent(self, e):
        if e.timerId() == self.timer.timerId():
            if self.isStart:
                self.field.update()
                self.update()

        else:
            super(Board, self).timerEvent(e)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        self.drawRectangles(painter)

    def keyPressEvent(self, e):#e means event
        if e.key() == Qt.Key_Space:
            if not self.isStart:
                self.isStart = True
                self.msgStatBar.emit(str('Go'))
            else:
                self.isStart = False
                self.msgStatBar.emit(str('Stop'))
        else:
            super(Board, self).keyPressEvent(e)

    def drawRectangles(self, qp):

        col = QColor(0, 0, 0)#borderline colour
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)#create pen wich has colour col(borderline between rectangles)
        victims = self.field.victims
        predators = self.field.predators
        walls = self.field.walls


        for v in victims:
            icon = QPixmap('GUI\\gop.bmp')
            qp.setBrush(QColor(245, 245, 245))#put brush that colour for victims
            qp.drawRect(v.x * self.squareWidth(), v.y * self.squareHeight(), self.squareWidth(), self.squareHeight())#first two - begin coordinates, last two end coord
            qp.drawPixmap(v.x * self.squareWidth(), v.y * self.squareHeight(), self.squareWidth(), self.squareHeight(),icon)#the same for image
        for p in predators:

            icon = QPixmap('GUI\\ment.bmp')
            qp.setBrush(QColor(200, 200, 200))
            qp.drawRect(p.x * self.squareWidth(), p.y * self.squareHeight(), self.squareWidth(), self.squareHeight())
            qp.drawPixmap(p.x * self.squareWidth(), p.y * self.squareHeight(), self.squareWidth(), self.squareHeight(),
                          icon)

        for w in walls:
            icon = QPixmap('GUI\\semki.bmp')
            qp.setBrush(QColor(240, 240, 200))
            qp.drawRect(w.x * self.squareWidth(), w.y * self.squareHeight(), self.squareWidth(), self.squareHeight())
            qp.drawPixmap(w.x * self.squareWidth(), w.y * self.squareHeight(), self.squareWidth(), self.squareHeight(),
                          icon)
    def squareWidth(self):
        return self.contentsRect().width() // Board.BoardWidth#for window size changes
    def squareHeight(self):
        return self.contentsRect().height() // Board.BoardHeight

class Scene(QMainWindow):

    def __init__(self, field):
        super().__init__()

        self.field = field
        self.initUI()
        #self.numV, self.numP, self.numW = numV, numP, numW

    def initUI(self):

        self.tboard = Board(self)#object tboard of class board
        #self.setCentralWidget( self.tboard )#make board the main widjet

        self.tboard.setGeometry(0,100,700,600)
        self.statusbar = self.statusBar()#string on the bottom of the window
        self.tboard.msgStatBar[str].connect(self.statusbar.showMessage)

        self.tboard.start()

        lblV = QLabel('Number of Victims', self)
        lblV.move(430, 0)
        lblP = QLabel('Number of predators', self)
        lblP.move(430, 20)
        lblW = QLabel('Number of walls', self)
        lblW.move(430, 40)



        sldV = QSlider(Qt.Horizontal, self)
        sldV.setValue(self.field.numV)
        sldV.setRange(1, 10)
        sldV.setGeometry(10, 10, 400, 20)
        sldV.valueChanged[int].connect(self.changeValueV)

       # lcdV = QLCDNumber(self)
       # lcdV.setGeometry(600, 10, 30, 30)
       # sldV.valueChanged.connect(lcdV.display)

        sldP = QSlider(Qt.Horizontal, self)
        sldP.setValue(self.field.numP)
        sldP.setRange(1, 10)
        sldP.setGeometry(10, 30, 400, 20)

        sldP.valueChanged[int].connect(self.changeValueP)

        sldW = QSlider(Qt.Horizontal, self)
        sldW.setValue(self.field.numW)
        sldW.setRange(1, 10)
        sldW.setGeometry(10, 50, 400, 20)
        sldW.valueChanged[int].connect(self.changeValueW)

        #butt = QPushButton('ok')

        #self.tboard.start()
        self.resize(700,700)#set the size of the window
        self.center()

        self.setWindowTitle('Victims and Predators')
        self.show()#basic method of qmainwindow class wich shows our window on the screen



    def changeValueV(self, value):

        self.field.numV=value
        self.field.reinit()
        self.tboard.update()
        lbV = QLabel('hjhjh', self)
        lbV.move(60, 10)

    def changeValueP(self, value):
        self.field.numP = value
        self.field.reinit()
        self.tboard.update()

    def changeValueW(self, value):
        self.field.numW = value
        self.field.reinit()
        self.tboard.update()

                #def paintEvent(self, e):
#
 #      qp.begin(self)
  #      self.drawRectangles(qp)
   #     qp.end()

    def center(self):
        screen = QDesktopWidget().screenGeometry()#all foo show window at the center
        size = self.geometry()
        self.move( (screen.width() - size.width())/2, (screen.height() - size.height())/2)
