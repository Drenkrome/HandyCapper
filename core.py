# Based
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QIcon, QPixmap
from UI import Ui_MainWindow
import os

# Custom imports
from module import parsing
from module import analysis


class MainWindow(QMainWindow):
    sports = ["hockey", "handball", "football"]
    room = ["fonbet", "betboom", "winline"]
    selected = ""

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tuning = 5
        # Set icon
        self.my_pixmap = QPixmap("icon.png")
        my_icon = QIcon(self.my_pixmap)
        self.setWindowIcon(my_icon)

        #                    Connection test
        res = parsing.runtest(self.ui)
        if res:
            self.ui.statusbar_txt.setText("Connection success!")

        #                     Bind elements
        # Type combo
        self.ui.type_box.addItems(self.sports)
        # Bookmaker combo
        self.ui.room_box.addItems(self.room)
        # Sport archive type combo
        self.ui.arch_sport_box.addItems(self.sports)
        self.ui.arch_sport_box.currentTextChanged.connect(lambda: self.myFiles())
        # Get button
        self.ui.get_btn.pressed.connect(lambda: parsing.makeurl(
            self.ui, self.ui.type_box.currentText(), self.ui.room_box.currentText()))
        # Archive button
        self.ui.get_arch_btn.pressed.connect(
            lambda: parsing.parse_archive(self.ui, self.ui.arch_sport_box.currentText(), int(self.ui.days_txt.text())))
        self.ui.plus_btn.pressed.connect(lambda: self.ui.days_txt.setText(str(int(self.ui.days_txt.text())+1)))
        self.ui.minus_btn.pressed.connect(lambda: self.ui.days_txt.setText(str(int(self.ui.days_txt.text())-1)))

        self.ui.arch_date_txt.setText("")
        self.myFiles()
        # Analysis block
        self.ui.analysis_box.addItems(self.sports)
        self.ui.calc_btn.pressed.connect(lambda: analysis.complex_run(
            self.ui.analysis_box.currentText(), self.ui, self.tuning))
        self.ui.show_btn.pressed.connect(lambda: self.resultWindow())
        # Tuning
        self.ui.tuning_txt.setText(str(self.tuning))
        self.ui.plus_btn_2.pressed.connect(lambda: self.tune("+"))
        self.ui.minus_btn_2.pressed.connect(lambda: self.tune("-"))

    def tune(self, action):
        if action == "+":
            self.tuning += 1
            self.ui.tuning_txt.setText(str(self.tuning))
        elif action == "-":
            self.tuning -= 1
            self.ui.tuning_txt.setText(str(self.tuning))

    def resultWindow(self):
        msg = QMessageBox()
        msg.setWindowTitle("VALUE BETS")
        # Get filename
        directory = os.path.dirname(os.getcwd()) + "/HandyCapper/data/results/"
        files = os.listdir(directory)
        sport = self.ui.analysis_box.currentText()
        text = ""
        for file in files:
            type = file.split("_")[1]
            full = directory + file
            if type == sport + ".txt":
                with open(full) as file:
                    text = file.read()
                    break
        msg.setText(text)
        msg.my_pixmap = QPixmap("happy.png")
        my_icon = QIcon(msg.my_pixmap)
        msg.setWindowIcon(my_icon)
        msg.exec()

    def closeEvent(self, event):
        parsing.driver.quit()
        print("Webdriver shutdown...")

    def myFiles(self):
        sport = self.ui.arch_sport_box.currentText()
        dir_path = os.path.dirname(os.getcwd()) + r'/HandyCapper/data/archive/'
        # list to store files
        res = []
        # Iterate directory
        for file_path in os.listdir(dir_path):
            # check if current file_path is a file
            if os.path.isfile(os.path.join(dir_path, file_path)):
                # add filename to list
                res.append(file_path)

        if len(res) <= 1:
            self.ui.arch_date_txt.setText("No data")
        for i in res:
            date = i.split("_")
            if date[3] == sport + ".txt":
                self.ui.arch_date_txt.setText(date[1])
                break
            else:
                self.ui.arch_date_txt.setText("No data")


if __name__ == "__main__":
    # Instance of main window
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())
