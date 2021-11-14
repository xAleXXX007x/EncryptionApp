from PyQt5 import QtWidgets, uic
import sys
import os.path
import encoding

app = QtWidgets.QApplication([])

win = uic.loadUi("mainwindow.ui")
win.setFixedSize(win.geometry().width(), win.geometry().height())
win.selectedFile = ""

# Создание окна "О программе"
programInfo = """Смирнов Александр Алексеевич, ИСЭбд-41
Вариант №16 (4 задание)
Алгоритм: DES в режиме OFB (Output Feedback) обратная связь по выходу
DES (Data Encryption Standard) - алгоритм для симметричного шифрования, разработанный фирмой IBM и утверждённый правительством США в 1977 году как официальный стандарт.
Размер блока для DES равен 64 битам. В основе алгоритма лежит сеть Фейстеля с 16 циклами (раундами) и ключом, имеющим длину 56 бит. 
Алгоритм использует комбинацию нелинейных (S-блоки) и линейных (перестановки E, IP, IP-1) преобразований.

OFB (Output Feedback) - Режим обратной связи по выходу. Один из вариантов использования симметричного блочного шифра. Особенностью режима является то, что в качестве входных данных для алгоритма блочного шифрования не используется само сообщение. Вместо этого блочный шифр используется для генерации псевдослучайного потока байтов, который с помощью операции XOR складывается с блоками открытого текста.
"""

def showHelp():
  QtWidgets.QMessageBox.information(win, "О программе", programInfo)

win.actionHelp.triggered.connect(showHelp)

# Загрузка ключа из файла
def loadKeyFile():
  # Выбор файла
  fileName, _ = QtWidgets.QFileDialog.getOpenFileName(win, filter="Текстовые файлы (*.txt)")

  if (not fileName):
    return

  # Установка ключа в поле для ввода
  with open(fileName, "r") as file:
    win.entryKey.setPlainText(file.read())

win.buttonKeyFile.clicked.connect(loadKeyFile)

# Выбор файла для зашифровки / расшифровки
def selectFile():
  fileName, _ = QtWidgets.QFileDialog.getOpenFileName(win)
  
  if (not fileName):
    return

  # Отображение названия выбранного файла в окне
  win.labelFileName.setText(fileName)

  # Установка выбранного файла
  win.selectedFile = fileName

win.buttonSelectFile.clicked.connect(selectFile)

# Зашифровка выбранного файла
def encodeFile():
  # Считывание ключа из поля для ввода
  key = win.entryKey.toPlainText()

  if (not os.path.isfile(win.selectedFile)):
    error("Не выбран файл")
    return

  if (key == ""):
    error("Не указан ключ")
    return
  
  if (len(key) != 7):
    error("Ключ должен иметь длину в 7 символов (56 бит)")
    return

  # Выбор директории и названия для сохранения файла
  fileName, _ = QtWidgets.QFileDialog.getSaveFileName(win, directory=os.path.splitext(win.selectedFile)[0] + ".bin")

  if (not fileName):
    return

  encoded = ""

  # Считывание байтов файла
  with open(win.selectedFile, "rb") as file:
    bytes = file.read()
    # Шифрование файла
    # В качестве демонстрации инициализирующий вектор эквивалентен ключу
    encoded = encoding.encodeDES(bytes, win.entryKey.toPlainText(), win.entryKey.toPlainText())
    file.close()
  
  # Запись закодированных байтов в файл
  with open(fileName, "wb") as file:
    file.write(encoded)
    file.close()
  
  info("Файл успешно сохранён!")

win.buttonEncode.clicked.connect(encodeFile)

# Расшифровка выбранного файла
def decodeFile():
  key = win.entryKey.toPlainText()
  if (not os.path.isfile(win.selectedFile)):
    error("Не выбран файл")
    return

  if (key == ""):
    error("Не указан ключ")
    return
  
  if (len(key) != 7):
    error("Ключ должен иметь длину в 7 символов (56 бит)")
    return

  fileName, _ = QtWidgets.QFileDialog.getSaveFileName(win, directory=win.selectedFile)

  if (not fileName):
    return

  decoded = ""

  # Считывание байтов зашифрованного файла
  with open(win.selectedFile, "rb") as file:
    bytes = file.read()
    # Расшифрование файла
    decoded = encoding.decodeDES(bytes, win.entryKey.toPlainText(), win.entryKey.toPlainText())
    file.close()
  
  # Запись расшифрованных данных в файл
  with open(fileName, "wb") as file:
    file.write(decoded)
    file.close()
  
  info("Файл успешно сохранён!")

win.buttonDecode.clicked.connect(decodeFile)

def error(text):
  QtWidgets.QMessageBox.information(win, "Ошибка", text)

def info(text):
  QtWidgets.QMessageBox.information(win, "Информация", text)

if __name__ == "__main__":
  win.show()
  sys.exit(app.exec())
