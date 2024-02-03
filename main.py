from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QFontDialog, QColorDialog
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt6.QtCore import QFileInfo, Qt
from PyQt6.QtGui import QFont, QIcon
from NotePad import Ui_MainWindow


class NotePadMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionSave.triggered.connect(self.save_file)
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionPrint_preview.triggered.connect(self.print_preview)
        self.actionExport_PDF.triggered.connect(self.export_pdf)
        self.actionQuit.triggered.connect(self.quit_program)
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionBod.triggered.connect(self.set_bold)
        self.actionItalic.triggered.connect(self.set_italic)
        self.actionUnderline.triggered.connect(self.set_underline)
        self.actionLeft.triggered.connect(self.set_left_align)
        self.actionRight.triggered.connect(self.set_right_align)
        self.actionCenter.triggered.connect(self.set_center_align)
        self.actionJustify.triggered.connect(self.set_justify_align)
        self.actionFont.triggered.connect(self.set_font)
        self.actionColor.triggered.connect(self.set_color)
        self.actionAbout_Us.triggered.connect(self.about_us)

    def save_file(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File')
        if filename[0]:
            with open(filename[0], 'w') as file:
                text = self.textEdit.toPlainText()
                file.write(text)
                QMessageBox.about(self, 'Save File', 'File is saved!')

    def save_modify(self):
        if not self.textEdit.document().isModified():
            return True

        reuslt = QMessageBox.warning(self, 'File modified', 'File has been changed, do you want to save changes?',
                                     QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel)

        if reuslt == QMessageBox.StandardButton.Save:
            self.save_file()

        if reuslt == QMessageBox.StandardButton.Cancel:
            return True

        return True

    def new_file(self):
        if self.save_modify():
            self.textEdit.clear()

    def open_file(self):
        if not self.save_modify():
            return

        name_file = QFileDialog.getOpenFileName(self, 'Open File')  # directory='/home'
        if name_file[0]:
            with open(name_file[0], 'r') as file:
                self.textEdit.setText(file.read())

    def print_file(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer)

        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.textEdit.print(printer)

    def print_preview(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintPreviewDialog(printer, self)

        dialog.paintRequested.connect(self.preview_req)

        dialog.exec()

    def preview_req(self, printer):
        self.textEdit.print(printer)

    def export_pdf(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Export as PDF', 'Untitled.pdf')
        if file_name:
            if QFileInfo(file_name).suffix() == '':
                file_name = f'{file_name}.pdf'

            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_name)
            self.textEdit.document().print(printer)

    def quit_program(self):
        self.close()

    def set_bold(self):
        font = QFont()
        font.setBold(True)
        self.textEdit.setFont(font)

    def set_italic(self):
        font = QFont()
        font.setItalic(True)
        self.textEdit.setFont(font)

    def set_underline(self):
        font = QFont()
        font.setUnderline(True)
        self.textEdit.setFont(font)

    def set_left_align(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def set_right_align(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

    def set_center_align(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_justify_align(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignJustify)

    def set_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def set_color(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def about_us(self):
        QMessageBox.about(self, 'About App',
                          'This is a simple text editor written in python using Pyqt6 and Pyqt6-tools.\n\n'
                          'You can see more about the author and his works in his github page:\n\n'
                          'https://github.com/HB2102')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = NotePadMain()
    ui.show()
    sys.exit(app.exec())
