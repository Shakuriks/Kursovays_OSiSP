import tkinter as tk
from tkinter import filedialog, messagebox
from jinja2 import Template
import subprocess
import os
import datetime
import time
import re

# Функция для генерации лабораторной работы
def generate_random_report(tex_file_path, invoice_data):
    # Заменяем потенциально проблемные символы
    problem_characters = {
        '\u0301': "",  # Комбинированный акцент
        '\u2013': "-",  # Длинное тире (en-dash)
        '\u2014': "--",  # Длинное тире (em-dash)
        '\u2018': "'",  # Левый одиночный кавычки
        '\u2019': "'",  # Правый одиночный кавычки
        '\u201c': '"',  # Левые двойные кавычки
        '\u201d': '"',  # Правые двойные кавычки
        '\u2026': "...",  # Многоточие
        '\u2032': "'",  # Минутный штрих
        '\u2033': '"',  # Секундный штрих
        # Добавьте другие потенциально опасные символы здесь
    }
    
    cleaned_invoice_data = {
    clean_text(key, problem_characters): clean_text(value, problem_characters)
    for key, value in invoice_data.items()
    }

    with open(tex_file_path, 'r') as file:
        template_content = file.read()

    template = Template(template_content)
    rendered_content = template.render(cleaned_invoice_data)

# Используем asksaveasfilename для запроса имени файла и папки для сохранения
    save_path = filedialog.asksaveasfilename(
        title="Выберите имя файла и папку для сохранения",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not save_path:
        return  # Если пользователь отменил выбор, выходим из функции

    # Сохраняем LaTex-код в выбранное имя файла (заменяем на .tex)
    tex_path = "generated_report.tex"
    with open(tex_path, 'w') as output_file:
        output_file.write(rendered_content)


    # Генерируем PDF из LaTex
    subprocess.run(['pdflatex', tex_path])
    time.sleep(0.2)
    subprocess.run(['pdflatex', tex_path])
    time.sleep(0.2)
    subprocess.run(['pdflatex', tex_path])
    time.sleep(2)




    # Проверяем, сгенерирован ли файл PDF, и перемещаем его на выбранное место
    if os.path.exists("generated_report.pdf"):
        subprocess.run(['mv', "generated_report.pdf", save_path], check=True)
        
    # Удаляем временные файлы, если они существуют
    temp_files = ["generated_report.tex", "generated_report.aux", "generated_report.log", "generated_report.out", "generated_report.toc", "generated_report.fdb_latexmk", "generated_report.fls", "generated_report.synctex.gz"]
    remove_files(temp_files)

    messagebox.showinfo("Успех", f"Лабораторная работа сохранена как {save_path}")


# Функция для генерации лабораторной работы
def generate_lab(subject, lab_topic, lab_num, group_num, degree, student_name, professor_name, aims, theory, result, appendix_num, appendix_title, appendix):
    # Заменяем потенциально проблемные символы
    problem_characters = {
        '\u0301': "",  # Комбинированный акцент
        '\u2013': "-",  # Длинное тире (en-dash)
        '\u2014': "--",  # Длинное тире (em-dash)
        '\u2018': "'",  # Левый одиночный кавычки
        '\u2019': "'",  # Правый одиночный кавычки
        '\u201c': '"',  # Левые двойные кавычки
        '\u201d': '"',  # Правые двойные кавычки
        '\u2026': "...",  # Многоточие
        '\u2032': "'",  # Минутный штрих
        '\u2033': '"',  # Секундный штрих
        # Добавьте другие потенциально опасные символы здесь
    }
    
    fields_to_clean = [subject, lab_topic, lab_num, group_num, degree, student_name, professor_name, aims, theory, result, appendix_num, appendix_title, appendix]
    
    # Очищаем все поля от проблемных символов
    cleaned_fields = [clean_text(field, problem_characters) for field in fields_to_clean]
    
    # Распаковываем очищенные значения
    subject, lab_topic, lab_num, group_num, degree, student_name, professor_name, aims, theory, result, appendix_num, appendix_title, appendix = cleaned_fields

    invoice_data = {
        "subject": subject,
        "lab_topic": lab_topic,
        "lab_num": lab_num,
        "group_num": group_num,
        "year": str(datetime.datetime.now().year),
        "degree": degree,
        "student_name": student_name,
        "professor_name": professor_name,
        "aims": aims,
        "theory": theory,
        "result": result,
        "appendix_num": appendix_num,
        "appendix_title": appendix_title,
        "appendix": appendix
    }

    with open('lab_template/lab.tex', 'r') as file:
        template_content = file.read()

    template = Template(template_content)
    rendered_content = template.render(invoice_data)

# Используем asksaveasfilename для запроса имени файла и папки для сохранения
    save_path = filedialog.asksaveasfilename(
        title="Выберите имя файла и папку для сохранения",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not save_path:
        return  # Если пользователь отменил выбор, выходим из функции

    # Сохраняем LaTex-код в выбранное имя файла (заменяем на .tex)
    tex_path = "generated_lab.tex"
    with open(tex_path, 'w') as output_file:
        output_file.write(rendered_content)


    # Генерируем PDF из LaTex
    subprocess.run(['pdflatex', tex_path])
    time.sleep(0.2)
    subprocess.run(['pdflatex', tex_path])
    time.sleep(0.2)
    subprocess.run(['pdflatex', tex_path])
    time.sleep(2)




    # Проверяем, сгенерирован ли файл PDF, и перемещаем его на выбранное место
    if os.path.exists("generated_lab.pdf"):
        subprocess.run(['mv', "generated_lab.pdf", save_path], check=True)
        
    # Удаляем временные файлы, если они существуют
    temp_files = ["generated_lab.tex", "generated_lab.aux", "generated_lab.log", "generated_lab.out", "generated_lab.toc", "generated_lab.fdb_latexmk", "generated_lab.fls", "generated_lab.synctex.gz"]
    remove_files(temp_files)

    messagebox.showinfo("Успех", f"Лабораторная работа сохранена как {save_path}")


# Функция для удаления файлов, если они существуют
def remove_files(file_list):
    for file_name in file_list:
        if os.path.exists(file_name):
            os.remove(file_name)
            
# Функция для очистки текста от проблемных символов
def clean_text(text, problem_characters):
    for key, value in problem_characters.items():
        text = text.replace(key, value)
    return text


# Функция для вставки кода LaTex с выбранным изображением
def insert_image(target_widget):
    # Открываем диалоговое окно для выбора файла изображения
    filepath = filedialog.askopenfilename(
        title="Выберите изображение",
        filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("JPEG", "*.jpeg"), ("GIF", "*.gif"), ("BMP", "*.bmp"), ("TIFF", "*.tiff")]
    )
    
    if not filepath:
        return  # Если файл не выбран, просто возвращаемся
    
    # Форматируем путь для LaTex (заменяем обратные слеши на прямые)
    filepath = filepath.replace("\\", "/")
    
    # Текст с LaTex-кодом для вставки изображения
    code = f"""
\\begin{{figure}}[htbp]
    \centering
    \includegraphics[width=150mm,height=92mm]{{{filepath}}}
    \caption{{Подпись вашего изображения}}
\end{{figure}}
"""
    
    # Вставляем LaTex-код в целевой виджет
    target_widget.insert(tk.INSERT, code)
    
# Функция для вставки листинга кода
def insert_listing(target_widget):
    code = """
    \\begin{lstlisting}[caption=Подпись вашего листинга]
#include <stdio.h>

int main() /* Пример вашего кода" */
{ 
  printf("Hello world!"); 
  return 0;
}
\end{lstlisting}
"""
    
    # Вставляем текст на текущую позицию курсора в target_widget
    target_widget.insert(tk.INSERT, code)  # tk.INSERT определяет позицию курсора
    
def create_lab_gui():
    # Функция для генерации лабораторной работы
    def on_create_button_click():
        subject = subject_entry.get()
        lab_topic = lab_topic_entry.get()
        lab_num = lab_num_entry.get()
        group_num = group_num_entry.get()
        degree = degree_entry.get()
        student_name = student_name_entry.get()
        professor_name = professor_name_entry.get()
        aims = aims_text.get("1.0", tk.END).strip()
        theory = theory_text.get("1.0", tk.END).strip()
        result = result_text.get("1.0", tk.END).strip()
        appendix_num = appendix_num_entry.get()
        appendix_title = appendix_title_entry.get()
        appendix = appendix_text.get("1.0", tk.END).strip()

        if not all([subject, lab_topic, lab_num, group_num, student_name, professor_name, aims, theory, result, appendix_num, appendix_title, appendix]):
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все обязательные поля.")
            return

        generate_lab(subject, lab_topic, lab_num, group_num, degree, student_name, professor_name, aims, theory, result, appendix_num, appendix_title, appendix)

    # Создаем основное окно Tkinter и устанавливаем его размер
    new_window = tk.Toplevel()
    new_window.title("Создание лабораторной работы")
    new_window.geometry("900x900")  # Устанавливаем размер окна

    # Размер шрифта для меток и полей ввода
    font = ("Arial", 12)

    # Метки и поля ввода для необходимых аргументов
    tk.Label(new_window, text="Предмет:", font=font).grid(row=0, column=0, sticky='w')
    subject_entry = tk.Entry(new_window, font=font, width=90)  # Увеличиваем ширину
    subject_entry.grid(row=0, column=1, sticky='w')

    tk.Label(new_window, text="Тема лабораторной работы:", font=font).grid(row=1, column=0, sticky='w')
    lab_topic_entry = tk.Entry(new_window, font=font, width=90)  # Увеличиваем ширину
    lab_topic_entry.grid(row=1, column=1, sticky='w')

    tk.Label(new_window, text="Номер лабораторной работы:", font=font).grid(row=2, column=0, sticky='w')
    lab_num_entry = tk.Entry(new_window, font=font, width=90)  # Увеличиваем ширину
    lab_num_entry.grid(row=2, column=1, sticky='w')

    tk.Label(new_window, text="Номер группы:", font=font).grid(row=3, column=0, sticky='w')
    group_num_entry = tk.Entry(new_window, font=font, width=90)  # Увеличиваем ширину
    group_num_entry.grid(row=3, column=1, sticky='w')

    tk.Label(new_window, text="Имя студента:", font=font).grid(row=4, column=0, sticky='w')
    student_name_entry = tk.Entry(new_window, font=font, width=90)  # Увеличиваем ширину
    student_name_entry.grid(row=4, column=1, sticky='w')

    tk.Label(new_window, text="Имя профессора:", font=font).grid(row=5, column=0, sticky='w')
    professor_name_entry = tk.Entry(new_window, font=font, width=90)  # Увеличиваем ширину
    professor_name_entry.grid(row=5, column=1, sticky='w')

    tk.Label(new_window, text="Степень профессора (если есть):", font=font).grid(row=6, column=0, sticky='w')
    degree_entry = tk.Entry(new_window, font=font, width=90)  # Увеличиваем ширину
    degree_entry.grid(row=6, column=1, sticky='w')

    # Используем Text для больших полей ввода, увеличивая и ширину, и высоту
    tk.Label(new_window, text="Цель работы:", font=font).grid(row=7, column=0, sticky='w')
    aims_text = tk.Text(new_window, font=font, height=8, width=90)  # Увеличиваем и высоту, и ширину
    aims_text.grid(row=7, column=1, sticky='w')

    tk.Label(new_window, text="Теоретические сведения:", font=font).grid(row=8, column=0, sticky='w')
    theory_text = tk.Text(new_window, font=font, height=8, width=90)  # Увеличиваем и высоту, и ширину
    theory_text.grid(row=8, column=1, sticky='w')

    tk.Label(new_window, text="Результат выполнения программы:", font=font).grid(row=9, column=0, sticky='w')
    result_text = tk.Text(new_window, font=font, height=8, width=90)  # Увеличиваем и высоту, и ширину
    result_text.grid(row=9, column=1, sticky='w')

    tk.Label(new_window, text="Номер приложения:", font=font).grid(row=10, column=0, sticky='w')
    appendix_num_entry = tk.Entry(new_window, font=font, width=90)  # Увеличиваем ширину
    appendix_num_entry.grid(row=10, column=1, sticky='w')

    tk.Label(new_window, text="Название приложения:", font=font).grid(row=11, column=0, sticky='w')
    appendix_title_entry = tk.Entry(new_window, font=font, width=90)  # Увеличиваем ширину
    appendix_title_entry.grid(row=11, column=1, sticky='w')

    tk.Label(new_window, text="Содержание приложения:", font=font).grid(row=12, column=0, sticky='w')
    appendix_text = tk.Text(new_window, font=font, height=8, width=90)  # Увеличиваем и высоту, и ширину
    appendix_text.grid(row=12, column=1, sticky='w')

    # Кнопка, которая вызывает функцию `generate_lab`
    generate_button = tk.Button(new_window, text="Создать", font=font, command=on_create_button_click)
    generate_button.grid(row=13, column=1, sticky='e')
    
    # Указывает на активный элемент text
    current_focus = None
    
    # Создаем контекстное меню
    context_menu = tk.Menu(new_window, tearoff=0)  # tearoff=0 означает, что меню нельзя "открепить"
    context_menu.add_command(
        label="Вставить изображение",
        command=lambda: insert_image(current_focus)  # Вставка текста в активное поле
    )
    context_menu.add_command(
        label="Вставить листинг",
        command=lambda: insert_listing(current_focus)  # Вставка текста в активное поле
    )
    
    # Функция для отображения контекстного меню при нажатии правой кнопкой мыши
    def on_right_click(event):
        if current_focus is not None:
            context_menu.post(event.x_root, event.y_root)
            
    # Привязываем контекстное меню к нужным элементам
    aims_text.bind("<Button-2>", on_right_click)  # Нажатие правой кнопкой мыши
    theory_text.bind("<Button-2>", on_right_click)  # Нажатие правой кнопкой мыши
    result_text.bind("<Button-2>", on_right_click)  # Нажатие правой кнопкой мыши
    appendix_text.bind("<Button-2>", on_right_click)  # Нажатие правой кнопкой мыши
    
    # Функция для переключения состояния фокуса
    def on_focus_in(event):
        nonlocal current_focus
        current_focus = event.widget  # Теперь поле активно

    def on_focus_out(event):
        nonlocal current_focus
        current_focus = None  # Поле больше не активно
    
    # Привязываем обработчики фокуса к полям
    aims_text.bind("<FocusIn>", on_focus_in)
    aims_text.bind("<FocusOut>", on_focus_out)

    theory_text.bind("<FocusIn>", on_focus_in)
    theory_text.bind("<FocusOut>", on_focus_out)

    result_text.bind("<FocusIn>", on_focus_in)
    result_text.bind("<FocusOut>", on_focus_out)

    appendix_text.bind("<FocusIn>", on_focus_in)
    appendix_text.bind("<FocusOut>", on_focus_out)

    # Запускаем главный цикл приложения
    return new_window
    
#//////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////





# Функция, которая открывает диалоговое окно для выбора файла, затем создает динамический интерфейс для ввода данных
def create_random_report_gui():
    # Открываем диалоговое окно для выбора файла .tex
    tex_file_path = filedialog.askopenfilename(
        title="Выберите файл LaTex",
        filetypes=[("LaTex Files", "*.tex"), ("Все файлы", "*.*")]
    )

    if not tex_file_path:
        messagebox.showwarning("Ошибка", "Файл не был выбран.")
        return

    # Читаем содержимое файла .tex
    with open(tex_file_path, 'r') as tex_file:
        tex_content = tex_file.read()

    # Ищем все конструкции с двойными фигурными скобками
    placeholders = re.findall(r'{{(.+?)}}', tex_content)
    
    # Удаляем пробелы в начале и в конце строк
    placeholders = [p.strip() for p in placeholders]
    placeholders = [p.replace('{', '') for p in placeholders]
    placeholders = [p.replace('}', '') for p in placeholders]

    # Создаем словарь с пустыми значениями для найденных placeholders
    placeholder_dict = {placeholder: "" for placeholder in placeholders}

    # Создаем новое окно Tkinter для ввода значений в placeholders
    new_window = tk.Toplevel()  # Создаем новое окно
    new_window.title("Заполнение значений")

    # Создаем метки и поля ввода для каждого placeholder
    entry_dict = {}  # Словарь для хранения виджетов ввода

    for idx, placeholder in enumerate(placeholders):
        label = tk.Label(new_window, text=f"Введите значение для {{ {placeholder} }}:")
        label.grid(row=idx, column=0, sticky='w')

        text_entry = tk.Text(new_window, height=2, width=50)
        text_entry.grid(row=idx, column=1, sticky='w')

        # Сохраняем виджет в словаре для последующей обработки
        entry_dict[placeholder] = text_entry

    # Функция, которая сохраняет введенные значения в placeholder_dict
    def save_values():
        for placeholder, text_entry in entry_dict.items():
            value = text_entry.get("1.0", tk.END).strip()  # Получаем введенное значение
            placeholder_dict[placeholder] = value

        generate_random_report(tex_file_path, placeholder_dict)
        messagebox.showinfo("Сохранено", "Значения сохранены!")

    # Кнопка для сохранения значений
    save_button = tk.Button(
        new_window,
        text="Сохранить",
        command=save_values
    )
    save_button.grid(row=len(placeholders), column=1, sticky='e')










#//////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////

# Создаем главное окно Tkinter
root = tk.Tk()
root.title("Создание отчетов")

# Размер окна
root.geometry("300x200")

# Кнопка для создания отчета по лабораторной работе
lab_report_button = tk.Button(
    root,
    text="Создать отчет по лабораторной работе",
    command=create_lab_gui
)
lab_report_button.pack(pady=20)  # Устанавливаем вертикальный отступ

# Кнопка для создания отчета по своему шаблону
custom_report_button = tk.Button(
    root,
    text="Создать отчет по своему шаблону",
    command=create_random_report_gui
)
custom_report_button.pack(pady=20)  # Устанавливаем вертикальный отступ

# Запускаем главный цикл Tkinter
root.mainloop()