from flask import Flask, render_template, request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import re
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Задайте URI для вашей БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=False, nullable=False)

# Создание базы данных и таблиц
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')

#проверка адреса
def validate_email(email):
  regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
  if re.match(regex, email):
    return True
  else:
    return False

# Маршрут для обработки формы
@app.route('/submit', methods=['POST'])
def submit_form():
    # Получаем данные из формы
    email = request.form.get('textInput')
    if email:
      email = email.lower()  
      email = email.strip()
      
      if validate_email(email):
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is not None:
          return 'Такой пользователь уже существует. Попробуйте другой email'
        else:
          # Создаем новую запись
          new_user = User(email=email)
      
          # Добавляем запись в базу данных
          db.session.add(new_user)
          db.session.commit()
        # return 'ok'
        return redirect(url_for('index'))
      else:
        return "Ошибка добавления email в базу данных. Попробуйте еще раз."   
    else:
      return "Поле email пустое."




# email = input("Введите email: ")
# if validate_email(email):
#   print("Email-адрес корректен.")
# else:
#   print("Email-адрес некорректен.")

#     # Перенаправляем на главную страницу или другую страницу
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
