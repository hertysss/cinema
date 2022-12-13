from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QSpinBox, QDialogButtonBox, QComboBox, QListWidget, \
    QDateTimeEdit


class Add_cinema_dialog(QDialog):
    def __init__(self, ts):
        super().__init__()
        self.ts = ts
        cinemas = self.ts.get_cinemas()
        self.setWindowTitle("Добавление кинотеатра")
        self.setGeometry(600, 400, 400, 100)
        self.layout = QFormLayout(self)

        self.cinema_name = QLineEdit(self)
        self.layout.addRow('Название кинотеатра', self.cinema_name)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.layout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def getData(self):
        return self.cinema_name.text()


class Add_hall_dialog(QDialog):
    def __init__(self, ts):
        super().__init__()
        self.ts = ts
        self.cinemas = self.ts.get_cinemas()
        self.setWindowTitle("Добавление кинозала")
        self.setGeometry(600, 400, 400, 300)
        self.layout = QFormLayout(self)

        self.lw_cinema = QListWidget(self)
        self.lw_cinema.addItems(self.cinemas)
        self.layout.addRow('Название кинотеатра', self.lw_cinema)

        self.hall_name = QLineEdit(self)
        self.layout.addRow('Название кинозала', self.hall_name)

        self.rows = QSpinBox(self)
        self.rows.setMinimum(1)
        self.rows.setMaximum(20)
        self.rows.setValue(5)
        self.layout.addRow('Количество рядов', self.rows)

        self.cols = QSpinBox(self)
        self.cols.setMinimum(1)
        self.cols.setMaximum(20)
        self.cols.setValue(5)
        self.layout.addRow('Количество мест в ряду', self.cols)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.layout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def getData(self):
        return self.lw_cinema.currentItem().text(), self.hall_name.text(), int(self.rows.text()), int(self.cols.text())


class Add_session_dialog(QDialog):
    def __init__(self, ts):
        super().__init__()
        self.ts = ts
        self.cinemas = self.ts.get_cinemas()
        self.halls = []
        self.films = self.ts.get_films()
        self.setWindowTitle("Добавление сеанса")
        self.setGeometry(600, 400, 400, 400)
        self.layout = QFormLayout(self)

        self.lw_cinema = QListWidget(self)
        self.lw_cinema.addItems(self.cinemas)
        self.layout.addRow('Название кинотеатра', self.lw_cinema)

        self.lw_hall = QListWidget(self)
        self.lw_hall.addItems(self.halls)
        self.layout.addRow('Название кинозала', self.lw_hall)

        self.lw_film = QListWidget(self)
        self.lw_film.addItems(self.films)
        self.layout.addRow('Название фильма', self.lw_film)

        self.start_time = QDateTimeEdit()
        self.start_time.setDateTime(QDateTime.currentDateTime())
        self.layout.addRow('Время начала', self.start_time)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.layout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.check)
        self.buttonBox.rejected.connect(self.reject)
        self.lw_cinema.clicked.connect(self.hall_set)

    def hall_set(self, index):
        self.lw_hall.clear()
        cinema_name = index.data()
        self.halls = self.ts.get_halls(cinema_name)
        self.lw_hall.addItems(self.halls)

    def check(self):
        if (self.lw_cinema.currentRow() != -1 and self.lw_hall.currentRow() != -1
                and self.lw_film.currentRow() != -1 and self.start_time.text()):
            self.accept()

    def getData(self):
        return self.lw_cinema.currentItem().text(), self.lw_hall.currentItem().text(), \
               self.lw_film.currentItem().text(), self.start_time.text()


class Add_film_dialog(QDialog):
    def __init__(self, ts):
        super().__init__()
        self.ts = ts
        self.setWindowTitle("Добавление фильма")
        self.setGeometry(600, 400, 400, 100)
        self.layout = QFormLayout(self)

        self.film_name = QLineEdit(self)
        self.layout.addRow('Название фильма', self.film_name)

        self.duration = QSpinBox(self)
        self.duration.setMinimum(1)
        self.duration.setMaximum(200)
        self.duration.setValue(100)
        self.layout.addRow('Длительность в минутах', self.duration)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.layout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def getData(self):
        return self.film_name.text(), int(self.duration.text())

class Del_cinema_dialog(QDialog):
    def __init__(self, ts):
        super().__init__()
        self.ts = ts
        self.cinemas = self.ts.get_cinemas()
        self.setWindowTitle("Удаление кинотеатра")
        self.setGeometry(600, 400, 400, 200)
        self.layout = QFormLayout(self)

        self.lw_cinema = QListWidget(self)
        self.lw_cinema.addItems(self.cinemas)
        self.layout.addRow('Название кинотеатра', self.lw_cinema)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.layout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def getData(self):
        return self.lw_cinema.currentItem().text()

class Del_hall_dialog(QDialog):
    def __init__(self, ts):
        super().__init__()
        self.ts = ts
        self.cinemas = self.ts.get_cinemas()
        self.halls = []
        self.setWindowTitle("Удаление кинозала")
        self.setGeometry(600, 400, 400, 100)
        self.layout = QFormLayout(self)

        self.lw_cinema = QListWidget(self)
        self.lw_cinema.addItems(self.cinemas)
        self.layout.addRow('Название кинотеатра', self.lw_cinema)

        self.lw_hall = QListWidget(self)
        self.lw_hall.addItems(self.halls)
        self.layout.addRow('Название кинозала', self.lw_hall)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.layout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.check)
        self.buttonBox.rejected.connect(self.reject)
        self.lw_cinema.clicked.connect(self.hall_set)

    def hall_set(self, index):
        self.lw_hall.clear()
        cinema_name = index.data()
        self.halls = self.ts.get_halls(cinema_name)
        self.lw_hall.addItems(self.halls)

    def check(self):
        if self.lw_cinema.currentRow() != -1 and self.lw_hall.currentRow() != -1:
            self.accept()

    def getData(self):
        return self.lw_cinema.currentItem().text(), self.lw_hall.currentItem().text()

class Del_session_dialog(QDialog):
    def __init__(self, ts):
        super().__init__()
        self.ts = ts
        self.cinemas = self.ts.get_cinemas()
        self.halls = []
        self.sessions = []
        self.setWindowTitle("Удаление сеанса")
        self.setGeometry(600, 400, 400, 100)
        self.layout = QFormLayout(self)

        self.lw_cinema = QListWidget(self)
        self.lw_cinema.addItems(self.cinemas)
        self.layout.addRow('Название кинотеатра', self.lw_cinema)

        self.lw_hall = QListWidget(self)
        self.lw_hall.addItems(self.halls)
        self.layout.addRow('Название кинозала', self.lw_hall)

        self.lw_session = QListWidget(self)
        self.lw_session.addItems(self.sessions)
        self.layout.addRow('Сеанс', self.lw_session)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.layout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.check)
        self.buttonBox.rejected.connect(self.reject)
        self.lw_cinema.clicked.connect(self.hall_set)
        self.lw_hall.clicked.connect(self.session_set)

    def hall_set(self, index):
        self.lw_hall.clear()
        cinema_name = index.data()
        self.halls = self.ts.get_halls(cinema_name)
        self.lw_hall.addItems(self.halls)

    def session_set(self, index):
        self.lw_session.clear()
        hall_name = index.data()
        cinema_name = self.lw_cinema.currentItem().text()
        self.sessions = self.ts.get_sessions(cinema_name, hall_name)
        self.lw_session.addItems(self.sessions)

    def check(self):
        if (self.lw_cinema.currentRow() != -1 and self.lw_hall.currentRow() != -1
                and self.lw_session.currentRow() != -1):
            self.accept()

    def getData(self):
        return self.lw_cinema.currentItem().text(), self.lw_hall.currentItem().text(), \
               self.lw_session.currentItem().text()

class Del_film_dialog(QDialog):
    def __init__(self, ts):
        super().__init__()
        self.ts = ts
        self.films = self.ts.get_films()
        self.setWindowTitle("Удаление фильма")
        self.setGeometry(600, 400, 400, 300)
        self.layout = QFormLayout(self)

        self.lw_film = QListWidget(self)
        self.lw_film.addItems(self.films)
        self.layout.addRow('Название фильма', self.lw_film)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.layout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def getData(self):
        return self.lw_film.currentItem().text()