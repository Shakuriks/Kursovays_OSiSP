from jinja2 import Template
import subprocess
import os
import datetime

def generate_lab(subject, lab_topic, lab_num, group_num, degree, student_name, professor_name, aims, theory, appendix_num, appendix_title, appendix):
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
        "appendix_num": appendix_num,
        "appendix_title": appendix_title,
        "appendix": appendix
    }

    with open('lab_template/lab.tex', 'r') as file:
        template_content = file.read()

    template = Template(template_content)
    rendered_content = template.render(invoice_data)

    with open('generated_lab.tex', 'w') as output_file:
        output_file.write(rendered_content)
        
    # Компилируем LaTeX в PDF
    subprocess.run(['pdflatex', 'generated_lab.tex'])

    # Перемещаем созданный PDF файл в папку проекта
    project_folder = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(['mv', 'generated_lab.pdf', os.path.join(project_folder, 'generated_lab.pdf')])

    print("Лабораторная сгенерирована успешно.")

# Пример использования
generate_lab("Методы трансляции", "Синтаксический анализатор", "3", "153502",
                 "", "Легоньков Н.В.", "Гриценко Н.Ю.", "Не соснуть хуйца", "Теория хуйни", "А", "Листинг кода", "Python listing code")
