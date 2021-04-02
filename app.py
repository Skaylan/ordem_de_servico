from os import read
from typing import List
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import * 
import sqlite3





db = sqlite3.connect('database.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS cadastro(_id INTEGER PRIMARY KEY AUTOINCREMENT, cliente TEXT NOT NULL, contato TEXT, aparelho TEXT NOT NULL, servico TEXT NOT NULL, preco REAL, data TEXT NOT NULL)")

#Functions here
def push_button_save():
    id = None
    nome = form.lineEdit.text()
    contato = form.lineEdit_2.text()
    aparelho = form.lineEdit_3.text()
    servico = form.lineEdit_4.text()
    preco = form.lineEdit_5.text()
    data = form.lineEdit_6.text()
    
    try:
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute("INSERT INTO cadastro VALUES(?, ?, ?, ?, ?, ?, ?)", (id, nome, contato, aparelho, servico, preco, data))
        db.commit()
        db.close()
    except Exception as erro:
        print(f'Ocorreu um erro {erro}')


    form.lineEdit.setText('')
    form.lineEdit_2.setText('')
    form.lineEdit_3.setText('')
    form.lineEdit_4.setText('')
    form.lineEdit_5.setText('')
    form.lineEdit_6.setText('')

def call_list_frame():
    list.show()
    list.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    # list.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM cadastro")
    data = cursor.fetchall()
    list.tableWidget.setRowCount(len(data))
    list.tableWidget.setColumnCount(7)
    for i in range(0, len(data)):
        for j in range(0, 7):
            list.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
    db.commit()
    db.close()


def delete_row():
    row = list.tableWidget.currentRow()
    list.tableWidget.removeRow(row)

    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("SELECT ROWID FROM cadastro")
    data = cursor.fetchall()
    id_value = data[row][0]
    cursor.execute(f"DELETE FROM cadastro WHERE ROWID={str(id_value)}")
    db.commit()
    db.close()


def edit_row():
    row = list.tableWidget.currentRow()
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("SELECT ROWID FROM cadastro")
    data = cursor.fetchall()
    global _id
    _id = data[row][0]
    cursor.execute(f"SELECT * FROM cadastro WHERE ROWID={str(_id)}")
    selected_row = cursor.fetchall()
    cliente = selected_row[0][1]
    contato = selected_row[0][2]
    aparelho = selected_row[0][3]
    servico = selected_row[0][4]
    preco = selected_row[0][5]
    date = selected_row[0][6]
    edit.show()

    edit.lineEdit_6.setText(str(cliente))
    edit.lineEdit_2.setText(str(contato))
    edit.lineEdit_4.setText(str(aparelho))
    edit.lineEdit_5.setText(str(servico))
    edit.lineEdit_7.setText(str(preco))
    edit.lineEdit_3.setText(str(date))


def save_edited_row():

    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    id = None
    nome = edit.lineEdit_6.text()
    contato = edit.lineEdit_2.text()
    aparelho = edit.lineEdit_4.text()
    servico = edit.lineEdit_5.text()
    preco = edit.lineEdit_7.text().replace(',', '.')
    data = edit.lineEdit_3.text()

    # cursor.execute(f"UPDATE cadastro SET _id={id} WHERE ROWID={_id}")
    cursor.execute(f"UPDATE cadastro SET cliente =  '{str(nome)}' WHERE ROWID={_id}")
    cursor.execute(f"UPDATE cadastro SET contato = '{str(contato)}' WHERE ROWID={_id}")
    cursor.execute(f"UPDATE cadastro SET aparelho = '{str(aparelho)}' WHERE ROWID={_id}")
    cursor.execute(f"UPDATE cadastro SET sevico = '{str(servico)}' WHERE ROWID={_id}")
    cursor.execute(f"UPDATE cadastro SET preco = {float(preco)} WHERE ROWID={_id}")
    cursor.execute(f"UPDATE cadastro SET data = '{str(data)}' WHERE ROWID={_id}")
    db.commit()
    edit.close()


#Main app
app = QtWidgets.QApplication([])
form = uic.loadUi('formulario.ui')
list = uic.loadUi('listagem2.ui')
edit = uic.loadUi('edit.ui')

#Action buttons
form.pushButton.clicked.connect(push_button_save)
form.pushButton_2.clicked.connect(call_list_frame)
list.pushButton_3.clicked.connect(delete_row)
list.pushButton.clicked.connect(edit_row)
edit.pushButton.clicked.connect(save_edited_row)

#Widget configurations


form.show()
app.exec()