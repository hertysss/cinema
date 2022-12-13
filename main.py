import sys

from PyQt5 import uic
from PyQt5.QtCore import QDateTime, QModelIndex
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QListView, QTableWidget, QTableWidgetItem, \
    QAbstractItemView, QLineEdit, QInputDialog, QDialog, QTextBrowser, QDateTimeEdit, QListWidget, QTreeView, \
    QTreeWidget, QTreeWidgetItem, QListWidgetItem, QMessageBox

from cl_ticket_sys import Ticket_system
from cl_dialogs import Add_cinema_dialog, Add_hall_dialog, Add_film_dialog, Add_session_dialog, \
    Del_cinema_dialog, Del_hall_dialog, Del_film_dialog, Del_session_dialog

from funcs import *


GREEN = QColor(0, 255, 0)
RED = QColor(255, 0, 0)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_ui.ui', self)
        self.ts = self.load_data()

        self.lw_cinemas.clicked.connect(self.cinema_set)
        self.show_cinemas()
        self.lw_halls.clicked.connect(self.hall_set)
        self.lw_sessions.clicked.connect(self.session_set)

        self.tw_hall_plan.cellDoubleClicked.connect(self.buy_ticket)

        self.act_exit.triggered.connect(exit)

        self.act_add_cinema.triggered.connect(self.add_cinema)
        self.act_del_cinema.triggered.connect(self.del_cinema)

        self.act_add_hall.triggered.connect(self.add_hall)
        self.act_del_hall.triggered.connect(self.del_hall)

        self.act_add_session.triggered.connect(self.add_session)
        self.act_del_session.triggered.connect(self.del_session)

        self.act_add_film.triggered.connect(self.add_film)
        self.act_del_film.triggered.connect(self.del_film)

        self.act_find_session.triggered.connect(self.find_session)

    def load_data(self):
        #create_json()
        data = read_data()
        ts = Ticket_system(data)
        #init_data(ts)
        self.statusbar.showMessage("Данные загружены")
        return ts

    def find_session(self):
        current_datetime = QDateTime().currentDateTime()
        nearest_datetime = QDateTime(2030, 12, 31, 23, 59, 59)
        nearest_cinema_name = ""
        nearest_hall_name = ""
        for cinema_name in self.ts.get_cinemas():
            for hall_name in self.ts.get_halls(cinema_name):
                for start_time in self.ts.get_sessions(cinema_name, hall_name):
                    st = QDateTime().fromString(start_time, "dd.MM.yyyy HH:mm")
                    if current_datetime < st < nearest_datetime \
                            and self.ts.get_free_tickets(cinema_name, hall_name, start_time):
                        nearest_cinema_name = cinema_name
                        nearest_hall_name = hall_name
                        nearest_datetime = st

        nearest_datetime = nearest_datetime.toString("dd.MM.yyyy HH:mm")

        if nearest_cinema_name:
            print(f'{nearest_cinema_name}, {nearest_hall_name}, {nearest_datetime}')
            self.show_cinemas()

            for i in range(self.lw_cinemas.count()):
                cinema = self.lw_cinemas.item(i).text()
                if nearest_cinema_name == cinema:
                    self.lw_cinemas.setCurrentRow(i)
                    self.current_cinema_name = cinema

            halls = self.ts.get_halls(nearest_cinema_name)
            self.lw_halls.addItems(halls)

            for i in range(self.lw_halls.count()):
                hall = self.lw_halls.item(i).text()
                if nearest_hall_name == hall:
                    self.lw_halls.setCurrentItem(self.lw_halls.item(i))
                    self.current_hall_name = hall

            sessions = self.ts.get_sessions(nearest_cinema_name, nearest_hall_name)
            self.lw_sessions.addItems(sessions)

            for i in range(self.lw_sessions.count()):
                session = self.lw_sessions.item(i).text()
                if nearest_datetime == session:
                    self.lw_sessions.setCurrentItem(self.lw_sessions.item(i))
                    self.current_session = session

            self.tw_hall_plan.show()
            self.get_plan()

        else:
            self.statusbar.showMessage("Нет ближайшего сеанса")

    def show_cinemas(self):
        self.lw_cinemas.clear()
        self.lw_halls.clear()
        self.lw_sessions.clear()
        self.tw_hall_plan.hide()
        self.tb_info.clear()
        cinemas = self.ts.get_cinemas()
        self.lw_cinemas.addItems(cinemas)
        self.current_cinema_name = None
        self.current_hall_name = None
        self.current_session = None

    def cinema_set(self, index):
        self.lw_cinemas.setCurrentIndex(index)
        self.current_cinema_name = index.data()
        self.lw_halls.clear()
        self.lw_sessions.clear()
        self.tw_hall_plan.hide()
        self.tb_info.clear()
        halls = self.ts.get_halls(self.current_cinema_name)
        self.lw_halls.addItems(halls)

    def hall_set(self, index):
        self.lw_halls.setCurrentIndex(index)
        self.current_hall_name = index.data()
        self.lw_sessions.clear()
        self.tw_hall_plan.hide()
        self.tb_info.clear()
        sessions = self.ts.get_sessions(self.current_cinema_name, self.current_hall_name)
        self.lw_sessions.addItems(sessions)

    def session_set(self, index):
        self.lw_sessions.setCurrentIndex(index)
        self.current_session = index.data()
        self.tw_hall_plan.show()
        self.get_plan()

    def get_plan(self):
        if not self.current_session:
            return
        halls = self.ts.get_halls(self.current_cinema_name)
        rows = halls[self.current_hall_name]["rows"]
        cols = halls[self.current_hall_name]["cols"]
        self.tw_hall_plan.setRowCount(rows)
        self.tw_hall_plan.setColumnCount(cols)
        for row in range(rows):
            for col in range(cols):
                self.tw_hall_plan.setItem(row, col, QTableWidgetItem(f"ряд {row + 1}\nместо {col + 1}"))
                if self.ts.is_ticket_free(self.current_cinema_name,
                                          self.current_hall_name,
                                          self.current_session,
                                          row,
                                          col):
                    self.tw_hall_plan.item(row, col).setBackground(GREEN)
                else:
                    self.tw_hall_plan.item(row, col).setBackground(RED)
        self.tw_hall_plan.resizeRowsToContents()
        self.tw_hall_plan.resizeColumnsToContents()
        self.tw_hall_plan.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_hall_plan.clearSelection()

        self.get_session_info()

    def get_session_info(self):
        session = self.ts.get_session(self.current_cinema_name,self.current_hall_name,self.current_session)
        total_seats = session['rows'] * session['cols']
        free_seats = self.ts.get_free_tickets(self.current_cinema_name, self.current_hall_name, self.current_session)
        busy_seats = total_seats - free_seats
        self.tb_info.clear()
        self.tb_info.append(f"название фильма: {session['film_name']}")
        self.tb_info.append(f"начало сеанса: {session['start_time']}")
        self.tb_info.append(f"окончание сеанса: {session['end_time']}")
        self.tb_info.append(f"длительность сеанса: {session['duration']}")
        self.tb_info.append(f"стоимость билета: {session['price']}")
        self.tb_info.append(f"всего мест: {total_seats}")
        self.tb_info.append(f"занято мест: {busy_seats}")
        self.tb_info.append(f"свободно мест: {free_seats}")


    def buy_ticket(self, row, col):
        self.ts.change_ticket_status(self.current_cinema_name, self.current_hall_name, self.current_session, row, col)
        if self.ts.is_ticket_free(self.current_cinema_name, self.current_hall_name, self.current_session, row, col):
            self.tw_hall_plan.currentItem().setBackground(GREEN)
        else:
            self.tw_hall_plan.currentItem().setBackground(RED)
        self.tw_hall_plan.clearSelection()
        self.get_session_info()

    def add_cinema(self):
        cinema_dialog = Add_cinema_dialog(self.ts)
        if not cinema_dialog.exec():
            return
        cinema_name = cinema_dialog.getData()
        self.ts.add_cinema(cinema_name)
        self.show_cinemas()

    def del_cinema(self):
        cinema_dialog = Del_cinema_dialog(self.ts)
        if not cinema_dialog.exec():
            return
        cinema_name = cinema_dialog.getData()
        self.ts.delete_cinema(cinema_name)
        self.show_cinemas()

    def add_hall(self):
        hall_dialog = Add_hall_dialog(self.ts)
        if not hall_dialog.exec():
            return
        cinema_name, hall_name, rows, cols = hall_dialog.getData()
        self.ts.add_hall(cinema_name, hall_name, rows, cols)
        self.show_cinemas()

    def del_hall(self):
        hall_dialog = Del_hall_dialog(self.ts)
        if not hall_dialog.exec():
            return
        cinema_name, hall_name = hall_dialog.getData()
        self.ts.delete_hall(cinema_name, hall_name)
        self.show_cinemas()

    def add_session(self):
        session_dialog = Add_session_dialog(self.ts)
        if not session_dialog.exec():
            return
        cinema_name, hall_name, film_name, start_time = session_dialog.getData()
        self.ts.add_session(cinema_name, hall_name, film_name, start_time)
        self.show_cinemas()

    def del_session(self):
        session_dialog = Del_session_dialog(self.ts)
        if not session_dialog.exec():
            return
        cinema_name, hall_name, start_time = session_dialog.getData()
        self.ts.delete_session(cinema_name, hall_name, start_time)
        self.show_cinemas()

    def add_film(self):
        film_dialog = Add_film_dialog(self.ts)
        if not film_dialog.exec():
            return
        film_name, duration = film_dialog.getData()
        self.ts.add_film(film_name, duration)
        self.show_cinemas()

    def del_film(self):
        film_dialog = Del_film_dialog(self.ts)
        if not film_dialog.exec():
            return
        film_name = film_dialog.getData()
        self.ts.delete_film(film_name)
        self.show_cinemas()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())