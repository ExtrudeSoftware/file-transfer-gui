from utils import *
import client

class ClientGUI(QMainWindow):
	def __init__(self, parent=None):
		super(ClientGUI, self).__init__(parent)

		self.setupUI()


	def setupUI(self):

		self.setCentralWidget(self.layout())
		self.setStyleSheet(open("styles.qss", "r").read())
		self.setWindowTitle("client")

		self.setMaximumSize(650,650)
		self.setMinimumHeight(350)

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
		self.numLabel = QLabel("Random Number: ", self)

		self.ipLabel.setObjectName("two")
		self.numLabel.setObjectName("small")

		self.layoutVLabel.addWidget(self.portLabel)
		self.layoutVLabel.addWidget(self.ipLabel)
		self.layoutVLabel.addWidget(self.numLabel)

		self.layoutVLabel.setAlignment(Qt.AlignTop)
		self.layoutVLabel.setSpacing(30)

		return self.layoutVLabel


	def line_edits(self):
		self.layoutVLineEdit = QVBoxLayout()

		self.portLineEdit = QLineEdit()
		self.ipLineEdit = QLineEdit()
		self.numLineEdit = QLineEdit()

		self.portLineEdit.setPlaceholderText("Port")
		self.ipLineEdit.setPlaceholderText("Ip")
		self.numLineEdit.setPlaceholderText("Random Number")

		self.portLineEdit.setCursor(Qt.IBeamCursor)
		self.ipLineEdit.setCursor(Qt.IBeamCursor)
		self.numLineEdit.setCursor(Qt.IBeamCursor)

		self.layoutVLineEdit.addWidget(self.portLineEdit)
		self.layoutVLineEdit.addWidget(self.ipLineEdit)
		self.layoutVLineEdit.addWidget(self.numLineEdit)

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
		self.plainTextArea = QPlainTextEdit()

		self.plainTextArea.setReadOnly(True)

		return self.plainTextArea


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
		self.startButton.clicked.connect(self.send)

		self.installButton.setShortcut("CTRL+S")
		self.startButton.setShortcut("Enter")

		return self.layoutVPushButton


	def save_log(self):
		newFilePath, filterType = QFileDialog.getSaveFileName(self, "Save as...", "log.txt", "Log File")

		if newFilePath:
			self.file_path = newFilePath

			with open(self.file_path, "w") as f:
				f.write(self.plainTextArea.toPlainText())


	def status_bar(self):

		self.status = self.statusBar()
		self.status.showMessage("Client")


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
				self.s = client.SAWClient(self.ipLineEdit.text(), int(self.portLineEdit.text()))
				self.s.setup()
				self.s.connect()
				self.s.send_file(10, int(self.numLineEdit.text()))
			except ValueError:self.message_box_1();

		elif self.gbnCheckBox.isChecked():
			try:
				self.s = client.GBNClient(self.ipLineEdit.text(), int(self.portLineEdit.text()))
				self.s.setup()
				self.s.connect()
				self.s.send_file(10, int(self.numLineEdit.text()), 4)
			except ValueError:self.message_box_1();
		
		self.plainTextArea.clear()
		self.plainTextArea.setPlainText("Connected.")


	def uncheck(self, state):
		if state == Qt.Checked:
			if self.sender() == self.sawCheckBox:self.gbnCheckBox.setChecked(False)
			if self.sender() == self.gbnCheckBox:self.sawCheckBox.setChecked(False)	


	def layout(self):
		self.widget = QWidget()
		self.layoutG = QGridLayout()
		self.layoutH = QHBoxLayout()

		self.push_buttons()

		self.layoutH.addLayout(self.labels())
		self.layoutH.addLayout(self.line_edits())
		self.layoutG.addLayout(self.layoutH, 0, 0, 0, 1)
		self.layoutG.addWidget(self.startButton, 3, 0)
		self.layoutG.addLayout(self.check_boxes(), 2, 0)
		self.layoutG.addLayout(self.push_buttons(), 0, 2, 4, 2)

		self.widget.setLayout(self.layoutG)
		
		return self.widget


def main():
	import sys
	app = QApplication(sys.argv)
	win = ClientGUI()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()