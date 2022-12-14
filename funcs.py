import json


def read_data():
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


def create_json():
    with open("data.json", "w") as file:
        data = {"cinemas": {}, "films": {}}
        json.dump(data, file)

def create_report_timetable(session):
    pass

def init_data(ts):
    ts.add_cinema("Кинотеатр-1")
    ts.add_film("Фильм-1", 123)
    ts.add_film("Фильм-2", 114)
    ts.add_hall("Кинотеатр-1", "Первый")
    ts.add_session("Кинотеатр-1", "Первый", "Фильм-1", "07:00")
    ts.add_session("Кинотеатр-1", "Первый", "Фильм-2", "10:00")
    ts.add_session("Кинотеатр-1", "Первый", "Фильм-2", "12:00")

def print_dict(dct):
    for key, value in dct.items():
        print(key, value)




#ts.sale_ticket("Кинотеатр-1", "Первый", "07:00", 2, 2)
#print_dict(ts.get_tickets("Кинотеатр-1", "Первый", "07:00"))
#print()
#print_dict(ts.get_free_tickets("Кинотеатр-1", "Первый", "07:00"))
#print(ts.is_ticket_free("Кинотеатр-1", "Первый", "07:00", 0, 0))
