from datetime import timedelta, datetime
import json

class Ticket_system:
    def __init__(self, data):
        self.data = data
        self.cinemas = data.get("cinemas", {})
        self.films = data.get("films", {})

    def get_films(self):
        return self.films

    def get_film(self, film_name):
        return self.films.get(film_name, None)

    def get_cinemas(self):
        return self.cinemas

    def get_cinema(self, cinema_name):
        return self.cinemas.get(cinema_name, None)

    def get_halls(self, cinema_name):
        return self.cinemas[cinema_name]["halls"]

    def get_hall(self, cinema_name, hall_name):
        return self.cinemas[cinema_name]["halls"].get(hall_name, None)

    def get_sessions(self, cinema_name, hall_name):
        return self.cinemas[cinema_name]["halls"][hall_name]["sessions"]

    def get_session(self, cinema_name, hall_name, start_time):
        return self.cinemas[cinema_name]["halls"][hall_name]["sessions"].get(start_time, None)

    def get_tickets(self, cinema_name, hall_name, start_time):
        return self.cinemas[cinema_name]["halls"][hall_name]["sessions"][start_time]["tickets"]

    def get_ticket(self, cinema_name, hall_name, start_time, row, col):
        row, col = str(row), str(col)
        return self.cinemas[cinema_name]["halls"][hall_name]["sessions"][start_time]["tickets"][row][col]

    def get_free_tickets(self, cinema_name, hall_name, start_time):
        tickets = self.get_tickets(cinema_name, hall_name, start_time)
        count = 0
        for row, cols in tickets.items():
            for col, ticket in cols.items():
                if ticket["is_free"]:
                    count += 1
        return count

    def is_ticket_free(self, cinema_name, hall_name, start_time, row, col):
        row, col = str(row), str(col)
        return self.cinemas[cinema_name]["halls"][hall_name]["sessions"][start_time]["tickets"][row][col]["is_free"]

    def change_ticket_status(self, cinema_name, hall_name, start_time, row, col):
        row, col = str(row), str(col)
        if self.is_ticket_free(cinema_name, hall_name, start_time, row, col):
            self.cinemas[cinema_name]["halls"][hall_name]["sessions"][start_time]["tickets"][row][col]["is_free"] = False
        else:
            self.cinemas[cinema_name]["halls"][hall_name]["sessions"][start_time]["tickets"][row][col]["is_free"] = True
        self.save()
        return True

    def add_cinema(self, cinema_name):
        if cinema_name in self.cinemas:
            print("Кинотеатр с таким названием уже существует")
            return False
        self.cinemas[cinema_name] = {"name": cinema_name, "halls": {}}
        self.save()
        return True

    def add_film(self, film_name, duration):
        if film_name in self.films:
            print("Фильм с таким названием уже существует")
            return False
        self.films[film_name] = {"name": film_name, "duration": duration}
        self.save()
        return True

    def add_hall(self, cinema_name, hall_name, rows=7, cols=5):
        if hall_name in self.cinemas[cinema_name]["halls"]:
            print("Кинозал с таким названием уже существует")
            return False
        self.cinemas[cinema_name]["halls"][hall_name] = {"name": hall_name,
                                                         "rows": rows,
                                                         "cols": cols,
                                                         "sessions": {}}
        self.save()
        return True

    def add_session(self, cinema_name, hall_name, film_name, start_time, price=100):
        if start_time in self.cinemas[cinema_name]["halls"][hall_name]["sessions"]:
            print("Сеанс на это время уже существует")
            return False
        film = self.get_film(film_name)
        duration = film["duration"]
        mask = "%d.%m.%Y %H:%M"
        start_time = datetime.strftime(datetime.strptime(start_time, mask), mask)
        end_time = datetime.strftime(datetime.strptime(start_time, mask) + timedelta(minutes=duration), mask)
        rows = self.cinemas[cinema_name]["halls"][hall_name]["rows"]
        cols = self.cinemas[cinema_name]["halls"][hall_name]["cols"]
        if not self.check_session_time(cinema_name, hall_name, start_time, end_time):
            print("Сеанс не может быть добавлен")
            return False
        tickets = {str(row): {str(col): {"row": row,
                               "col": col,
                               "is_free": True} for col in range(cols)} for row in range(rows)}
        self.cinemas[cinema_name]["halls"][hall_name]["sessions"][start_time] = {"film_name": film_name,
                                                            "start_time": start_time,
                                                            "end_time": end_time,
                                                            "duration": duration,
                                                            "rows": rows,
                                                            "cols": cols,
                                                            "price": price,
                                                            "tickets": tickets}
        self.save()
        return True

    def check_session_time(self, cinema_name, hall_name, start_time, end_time):
        mask = "%d.%m.%Y %H:%M"
        start_time = datetime.strptime(start_time, mask)
        end_time = datetime.strptime(end_time, mask)
        sessions = self.get_sessions(cinema_name, hall_name)
        for session in sessions.values():
            st = datetime.strptime(session["start_time"], mask)
            et = datetime.strptime(session["end_time"], mask)
            if st <= start_time <= et or st <= end_time <= et:
                return False
        return True

    def delete_cinema(self, cinema_name):
        if cinema_name not in self.cinemas:
            print("Кинотеатра с таким названием нет")
            return False
        self.cinemas.pop(cinema_name)
        self.save()
        return True

    def delete_film(self, film_name):
        if film_name not in self.films:
            print("Фильма с таким названием нет")
            return False
        self.films.pop(film_name)
        self.save()
        return True

    def delete_hall(self, cinema_name, hall_name):
        if hall_name not in self.cinemas[cinema_name]["halls"]:
            print("Кинозала с таким названием нет")
            return False
        self.cinemas[cinema_name]["halls"].pop(hall_name)
        self.save()
        return True

    def delete_session(self, cinema_name, hall_name, start_time):
        if start_time not in self.cinemas[cinema_name]["halls"][hall_name]["sessions"]:
            print("Сеанса на это время нет")
            return False
        self.cinemas[cinema_name]["halls"][hall_name]["sessions"].pop(start_time)
        self.save()
        return True

    def save(self):
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file,
                      indent=4,
                      sort_keys=False,
                      ensure_ascii=False)

