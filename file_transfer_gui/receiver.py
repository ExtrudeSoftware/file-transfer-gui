from utils import *
import server

class ServerGUI(QMainWindow):
	def __init__(self, parent=None):
		super(ServerGUI, self).__init__(parent)

		self.setupUI()


	def setupUI(self):

		self.setCentralWidget(self.layout())
		self.setStyleSheet(open("styles.qss", "r").read())
		self.setWindowTitle("server")

		self.setMaximumSize(550,550)
		self.setMinimumHeight(300)

		self.status_bar()

		self.show()


	def check_boxes(self):
		self.layoutHCheckBox = QHBoxLayout()

		self.sawCheckBox = QCheckBox("SAW")
		self.gbnCheckBox = QCheckBox("GBN")

		self.sawCheckBox.setChecked(True)

		self.layoutHCheckBox.addWidget(self.sawCheckBox)
		self.layoutHCheckBox.addWidget(self.gbnCheckBox)

		self.sawCheckBox.setCursor(Qt.PointingHandCursor)
		self.gbnCheckBox.setCursor(Qt.PointingHandCursor)

		self.sawCheckBox.stateChanged.connect(self.uncheck)
		self.gbnCheckBox.stateChanged.connect(self.uncheck)

		return self.layoutHCheckBox

	
	def closeEvent(self, event):
		self.closeMsg = QMessageBox()

		self.closeMsg.setIcon(QMessageBox.Question)
		self.closeMsg.setWindowTitle("Quit?")
		self.closeMsg.setText("Are you sure you want to close the program??")
		self.closeMsg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		
		self.result = self.closeMsg.exec()

		if self.result == QMessageBox.Yes:event.accept()
		else:event.ignore()
		

	def labels(self):
		self.layoutVLabel = QVBoxLayout()

		self.portLabel = QLabel("Port: ", self)
		self.ipLabel = QLabel("Ip: ", self)

		self.ipLabel.setAlignment(Qt.AlignBottom)
		self.layoutVLabel.addWidget(self.portLabel)
		self.layoutVLabel.addWidget(self.ipLabel)

		self.layoutVLabel.setAlignment(Qt.AlignTop)
		self.layoutVLabel.setSpacing(22)

		return self.layoutVLabel


	def line_edits(self):
		self.layoutVLineEdit = QVBoxLayout()

		self.portLineEdit = QLineEdit()
		self.ipLineEdit = QLineEdit()

		self.portLineEdit.setPlaceholderText("Port")

		self.ipLineEdit.setText(socket.gethostbyname(socket.gethostname()))
		self.ipLineEdit.setReadOnly(True)

		self.portLineEdit.setCursor(Qt.IBeamCursor)

		self.layoutVLineEdit.addWidget(self.portLineEdit)
		self.layoutVLineEdit.addWidget(self.ipLineEdit)

		self.layoutVLineEdit.setAlignment(Qt.AlignTop)

		return self.layoutVLineEdit


	def message_box_1(self):
		self.portLineEdit.setObjectName("err")
		self.emptyError = QMessageBox()

		self.emptyError.setIcon(QMessageBox.Critical)
		self.emptyError.setWindowTitle("Port Error!")
		self.emptyError.setText("Please enter a valid port.")
		self.emptyError.setStandardButtons(QMessageBox.Ok)

		self.emptyError.exec()


	def message_box_2(self):
		self.portLineEdit.setObjectName("err")
		self.emptyError = QMessageBox()

		self.emptyError.setIcon(QMessageBox.Warning)
		self.emptyError.setWindowTitle("Warning")
		self.emptyError.setText("Please wait...")
		self.emptyError.setStandardButtons(QMessageBox.Ok)

		self.emptyError.exec()


	def plain_text_edit(self):
		self.plainTextArea2 = QPlainTextEdit()

		self.plainTextArea2.setReadOnly(True)

		return self.plainTextArea2


	def push_buttons(self):
		self.layoutVPushButton = QVBoxLayout()

		self.startButton = QPushButton()
		self.installButton = QPushButton()

		self.startButton.setText("Start")

		self.installButton.setIcon(QIcon("icons\install.png"))
		self.installButton.setText("Install Log")
		self.installButton.setObjectName("install")

		self.installButton.setCursor(Qt.PointingHandCursor)
		self.startButton.setCursor(Qt.PointingHandCursor)

		self.layoutVPushButton.addWidget(self.plain_text_edit())
		self.layoutVPushButton.addWidget(self.installButton)

		self.installButton.clicked.connect(self.save_log)
		self.startButton.clicked.connect(self.send);

		self.installButton.setShortcut("CTRL+S")
		self.startButton.setShortcut("Enter")

		return self.layoutVPushButton


	def save_log(self):
		newFilePath, filterType = QFileDialog.getSaveFileName(self, "Save as...", "log.txt", "Log File")

		if newFilePath:
			self.file_path = newFilePath

			with open(self.file_path, "w") as f:
				f.write(self.plainTextArea2.toPlainText())


	def on_connection(self, x, y):
		log = str(y) + " connected"
		self.plainTextArea2.setPlainText(log)


	def send(self):
		self.message_box_2()

		if len(self.portLineEdit.text()) <= 0:
			self.portLineEdit.setObjectName("err")
			self.emptyError = QMessageBox()

			self.emptyError.setIcon(QMessageBox.Critical)
			self.emptyError.setWindowTitle("Port Error!")
			self.emptyError.setText("Please enter the port.")
			self.emptyError.setStandardButtons(QMessageBox.Ok)

			self.emptyError.exec()
		
		elif self.sawCheckBox.isChecked():
			try:
				self.s = server.SAWServer(int(self.portLineEdit.text()), 1024)
				print(int(self.portLineEdit.text()))
				self.s.setup()
				sleep(3)
				self.s.start(self.on_connection)
			except ValueError:self.message_box_1();

		elif self.gbnCheckBox.isChecked():
			try:
				self.s = server.GBNServer(int(self.portLineEdit.text()), 1024)
				print(int(self.portLineEdit.text()))
				self.s.setup(4)
				sleep(3)
				self.s.start(self.on_connection)
			except ValueError:self.message_box_1();

		
				

	def status_bar(self):
		self.status = self.statusBar()
		self.status.showMessage("Server")


	def uncheck(self, state):
		if state == Qt.Checked:
			if self.sender() == self.sawCheckBox:self.gbnCheckBox.setChecked(False)
			if self.sender() == self.gbnCheckBox:self.sawCheckBox.setChecked(False)	

		
	def layout(self):
		self.widget = QWidget()
		self.layoutG = QGridLayout()
		self.layoutV = QVBoxLayout()
		self.layoutH = QHBoxLayout()

		self.push_buttons()

		self.layoutH.addLayout(self.labels())
		self.layoutH.addLayout(self.line_edits())
		self.layoutG.addLayout(self.layoutH, 0, 0, 0, 1)
		self.layoutG.addLayout(self.check_boxes(), 1, 0)
		self.layoutG.addWidget(self.startButton, 2, 0)
		self.layoutG.addLayout(self.push_buttons(), 0, 2, 3, 2)

		self.widget.setLayout(self.layoutG)
		
		return self.widget


def main():
	import sys
	app = QApplication(sys.argv)
	win = ServerGUI()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()