import json
from docx import Document
from docxtpl import DocxTemplate


def read_data():
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


def create_json():
    with open("data.json", "w") as file:
        data = {"cinemas": {}, "films": {}}
        json.dump(data, file)

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


def create_report_timetable(month_name, data):
    doc = DocxTemplate("template_report_timetable.docx")
    context = {"month_name": month_name,
               "data": data
               }
    doc.render(context)
    file_name = f"Расписание_сеансов_за_{month_name}.docx"
    doc.save(file_name)

