#!/usr/bin/env python3
# -*- config: utf-8 -*-


# Вариант 12. Использовать словарь, содержащий следующие ключи: фамилия, имя; номер телефона;
# дата рождения (список из трех чисел). Написать программу, выполняющую следующие
# действия: ввод с клавиатуры данных в список, состоящий из словарей заданной структуры;
# записи должны быть размещены по алфавиту; вывод на экран информации о людях, чьи
# дни рождения приходятся на месяц, значение которого введено с клавиатуры; если таких
# нет, выдать на дисплей соответствующее сообщение.


from tkinter import *
from tkinter import messagebox as mb
import indmodule
import sqlite3


def add_window():
    def add():
        brd = str(en3.get())
        name = en1.get()
        phone = en2.get()
        birthday = list(map(int, brd.split(',')))

        people.add(name, phone, birthday)

    add_w = Toplevel()
    add_w.title('Добавить')
    add_w.resizable(False, False)
    add_w.geometry('225x100')
    en1 = Entry(add_w)
    en2 = Entry(add_w)
    en3 = Entry(add_w)
    lb1 = Label(add_w, text="ФИО")
    lb2 = Label(add_w, text="Номер")
    lb3 = Label(add_w, text="Дата рождения")
    bt1 = Button(add_w, text="Добавить", command=add)

    lb1.grid(row=0, column=0)
    lb2.grid(row=1, column=0)
    lb3.grid(row=2, column=0)
    en1.grid(row=0, column=1)
    en2.grid(row=1, column=1)
    en3.grid(row=2, column=1)
    bt1.grid(row=3, column=0, columnspan=2)


# def load_window():
#     def load_f():
#         people.load(en4.get())
#         load_w.destroy()
#
#     load_w = Toplevel()
#     load_w.title('Сохранение')
#     load_w.resizable(False, False)
#     load_w.geometry('225x100')
#     lb4 = Label(load_w, text="Введите название файла")
#     en4 = Entry(load_w)
#     bt3 = Button(load_w, text="Загрузить", command=load_f)
#     lb4.pack(padx=2, pady=2)
#     en4.pack(padx=2, pady=2)
#     bt3.pack(padx=2, pady=2)


def update_window():
    def upd():
        row = en1.get()
        value = str(en2.get())
        col = ''
        if var.get() == 0:
            col = 'name'
        elif var.get() == 1:
            col = 'phone'
        elif var.get() == 2:
            col = 'day'
        elif var.get() == 3:
            col = 'month'
        elif var.get() == 4:
            col = 'year'
        print(type(col))
        cur.execute(f'''UPDATE peoples SET {col} = {value} WHERE rowid = {row}''')
        db.commit()

    upd_w = Toplevel()
    upd_w.title('Обновление')
    upd_w.resizable(False, False)
    upd_w.geometry('625x100')
    var = IntVar()
    var.set(0)
    rb1 = Radiobutton(upd_w, text="Фамилия", indicatoron=0, variable=var, value=0)
    rb2 = Radiobutton(upd_w, text="Номер телефона", indicatoron=0, variable=var, value=1)
    rb3 = Radiobutton(upd_w, text="День",  variable=var, indicatoron=0, value=2)
    rb4 = Radiobutton(upd_w, text="Месяц",  variable=var, indicatoron=0, value=3)
    rb5 = Radiobutton(upd_w, text="Год",  variable=var, indicatoron=0, value=4)
    lb1 = Label(upd_w, text='Выберите столбец таблицы для обновления:')
    lb2 = Label(upd_w, text='Введите номер строки, в которой будут обновлены данные:')
    lb3 = Label(upd_w, text='Введите новые данные:')
    en1 = Entry(upd_w, width=40)
    en2 = Entry(upd_w, width=40)
    bt = Button(upd_w, text='Обновить', command=upd)
    rb1.grid(row=0, column=1)
    rb2.grid(row=0, column=2)
    rb3.grid(row=0, column=3)
    rb4.grid(row=0, column=4)
    rb5.grid(row=0, column=5)
    lb1.grid(row=0, column=0, sticky=E)
    lb2.grid(row=2, column=0, sticky=E)
    lb3.grid(row=4, column=0, sticky=E)
    en1.grid(row=2, column=1, columnspan=5, sticky=W+E)
    en2.grid(row=4, column=1, columnspan=5, sticky=W+E)
    bt.grid(row=5, column=4, columnspan=2, sticky=E)


def del_window():
    def row_del():
        row = en1.get()
        print(row)
        cur.execute(f'''DELETE FROM peoples WHERE rowid = {row}''')

    del_w = Toplevel()
    del_w.title('Удаление')
    lb1 = Label(del_w, text='Введите строку:')
    en1 = Entry(del_w)
    bt = Button(del_w, text='УДАЛИТЬ', command=row_del)
    lb1.pack(padx=2, pady=2)
    en1.pack(padx=2, pady=2)
    bt.pack(padx=2, pady=2)


def help_window():
    help_w = Toplevel()
    help_w.title('ТЕБЕ НИЧЕГО УЖЕ НЕ ПОМОЖЕТ')
    help_w.resizable(False, False)
    help_w['bg'] = 'white'
    img = PhotoImage(file='wolf.png')
    bt2 = Button(
        help_w,
        image=img,
        bg='white',
        borderwidth=0,
        activebackground='white',
        command=lambda: help_w.destroy()
    )
    bt2.image = img
    bt2.pack()


def select_window():
    def choice():
        try:
            choice_en = int(en4.get())
            res = people.select(choice_en)
            if res:
                for idx, person in enumerate(res, 1):
                    text.delete(0.0, END)
                    text.insert(0.0, '{:>4}: {}'.format(idx, person.name))
            else:
                text.delete(0.0, END)
                text.insert(0.0, 'В этом месяце именинников нема')
        except(ValueError, TypeError):
            mb.showinfo("Выбор месяца",
                        "Введите месяц!")

    sel_w = Toplevel()
    sel_w.title('Выбрать')
    sel_w.resizable(False, False)
    sel_w.geometry('225x100')
    lb4 = Label(sel_w, text="Введите месяц")
    en4 = Entry(sel_w)
    bt3 = Button(sel_w, text="Подтвердить", command=choice)
    lb4.pack(padx=2, pady=2)
    en4.pack(padx=2, pady=2)
    bt3.pack(padx=2, pady=2)


def show():
    text.delete(0.0, END)
    text.insert(0.0, people)


if __name__ == '__main__':
    db = sqlite3.connect('ind.sqlite')
    cur = db.cursor()
    people = indmodule.People()

    root = Tk()
    root.geometry('800x450')
    root.title('Главное окно')
    root.resizable(False, False)

    main_menu = Menu(root)
    root.config(menu=main_menu)

    file_menu = Menu(main_menu, tearoff=0)
    file_menu.add_command(label="Загрузить", command=lambda: people.load())
    file_menu.add_command(label="Сохранить", command=lambda: people.save())
    file_menu.add_command(label="Обновить", command=update_window)
    file_menu.add_command(label="Удалить", command=del_window)

    main_menu.add_cascade(label="База данных", menu=file_menu)
    main_menu.add_command(label="Добавить", command=add_window)
    main_menu.add_command(label="Показать", command=show)
    main_menu.add_command(label="Выбрать", command=select_window)
    main_menu.add_command(label="Помощь", command=help_window)
    main_menu.add_command(label="Выход", command=lambda: root.destroy())

    text = Text(bg='white', width=97, height=100)
    text.pack(side=LEFT)
    scroll = Scrollbar(command=text.yview)
    scroll.pack(side=LEFT, fill=Y)
    text.config(yscrollcommand=scroll.set)

    root.mainloop()
