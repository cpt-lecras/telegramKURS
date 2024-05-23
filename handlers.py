from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
import requests
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import kb

router = Router()
base_url="http://127.0.0.1:8000"

@router.message(Command("start"))
async def start_handler(msg: Message):
    tt = "Привет {name} можешь тестировать!"
    await msg.answer(tt.format(name=msg.from_user.full_name), reply_markup=kb.mainmenu)
#----------------------------------------------------------FSM States for processes
class AddStudent(StatesGroup):
    waiting_for_name_surname = State()
class AddSubject(StatesGroup):
    waiting_for_subject_teacher = State()
class AddMark(StatesGroup):
    waiting_for_mark = State()
class GetMarks(StatesGroup):
    waiting_all_marks = State()
#----------------------------------------------------------Add Student
@router.message(F.text=="Добавить студента")
async def add_student(msg: types.Message, state: FSMContext):
    await state.set_state(AddStudent.waiting_for_name_surname)
    await msg.answer("Напиши Имя Фамилию студента", parse_mode=ParseMode.MARKDOWN_V2)
@router.message(AddStudent.waiting_for_name_surname)
async def get_name_surname(msg: types.Message, state: FSMContext):
    name_surname = msg.text
    name, surname = name_surname.split()
    requests.post(f"{base_url}/api/add_stud/{name}/{surname}/")
    await state.clear()
    await msg.answer(f"Студент {name} {surname} успешно добавлен!")

#----------------------------------------------------------Add Subj
@router.message(F.text=="Добавить предмет")
async def add_subj(msg: types.Message, state: FSMContext):
    await state.set_state(AddSubject.waiting_for_subject_teacher)
    await msg.answer("Напиши название предмета и фамилию учителя ", parse_mode=ParseMode.MARKDOWN_V2)
@router.message(AddSubject.waiting_for_subject_teacher)
async def get_name_teacher(msg: types.Message, state: FSMContext):
    name_teacher = msg.text
    name, teacher = name_teacher.split()
    requests.post(f"{base_url}/api/add_subj/{name}/{teacher}/")
    await state.clear()
    await msg.answer(f"Предмет {name} у {teacher} успешно добавлен!")


#----------------------------------------------------------Add Mark
@router.message(F.text=="Добавить оценку")
async def add_subj(msg: types.Message, state: FSMContext):
    await state.set_state(AddMark.waiting_for_mark)
    await msg.answer("Напиши поочередно [Имя Фамилия Предмет Оценка]", parse_mode=ParseMode.MARKDOWN_V2)
@router.message(AddMark.waiting_for_mark)
async def get_name_teacher(msg: types.Message, state: FSMContext):
    name_teacher = msg.text
    name, sur, subj, mark = name_teacher.split()
    requests.post(f"{base_url}/api/set_mark/{name}/{sur}/{subj}/{mark}/")
    await state.clear()
    await msg.answer(f"{sur} {name} получил по {subj} - {mark}")

#----------------------------------------------------------Get Students
@router.message(F.text=="Вывести студентов")
async def start_handler(msg: Message):
    response = requests.get(f"{base_url}/api/show_stud/")

    if response.status_code == 200:
        data = response.json()
        students_str = ""

        for student in data:
            name = student["name"]
            surname = student["surname"]
            student_id = student["id"]
            students_str += f"ID: {student_id}, Имя: {name}, Фамилия: {surname}\n"

        if students_str:
            await msg.answer(students_str, parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await msg.answer("Список студентов пуст.")
    else:
        await msg.answer(f"Ошибка: {response.status_code} - {response.text}")
#----------------------------------------------------------Get Sbj
@router.message(F.text=="Вывести предметы")
async def start_handler(msg: Message):
    response=requests.get(f"{base_url}/api/show_subj/")
    if response.status_code == 200:
        data = response.json()
        students_str = ""

        for sbj in data:
            name = sbj["name"]
            surname = sbj["teacher"]
            student_id = sbj["id"]
            students_str += f"ID: {student_id}, Предмет: {name}, Учитель: {surname}\n"

        if students_str:
            await msg.answer(students_str, parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await msg.answer("Список предметов пуст.")
    else:
        await msg.answer(f"Ошибка: {response.status_code} - {response.text}")

#----------------------------------------------------------Get Marks by ID
@router.message(F.text=="Вывести оценки ученика")
async def start_handler(msg: types.Message, state: FSMContext):
    await state.set_state(GetMarks.waiting_all_marks)
    await msg.answer("Напиши id ученика", parse_mode=ParseMode.MARKDOWN_V2)
@router.message(GetMarks.waiting_all_marks)
async def get_name_teacher(msg: types.Message, state: FSMContext):
    idp = msg.text
    response=requests.get(f"{base_url}/api/show_marks/{idp}")
    if response.status_code == 200:
        data = response.json()
        students_str = ""

        for mark in data:
            name = mark["name"]
            surname = mark["surname"]
            sbj = mark["subject"]
            marks = mark["mark"]
            students_str += (f"{surname} {name} \- {marks} по {sbj}\n")

        if students_str:
            await msg.answer(students_str, parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await msg.answer("Список предметов пуст.")
    else:
        await msg.answer(f"Ошибка: {response.status_code} - {response.text}")
    await state.clear()