"""Deterministic in-memory data for HW2. No database queries yet."""

USERS = [
    {"name": "Dr. Pepper", "initials": "DP", "avatar": "core/img/avatar-1.png"},
    {"name": "Bender", "initials": "B", "avatar": "core/img/avatar-2.png"},
    {"name": "V. Pupkin", "initials": "VP", "avatar": "core/img/avatar-3.png"},
    {"name": "Queen Victoria", "initials": "QV", "avatar": "core/img/avatar-4.png"},
    {"name": "Mr. Freeman", "initials": "MF", "avatar": "core/img/avatar-5.png"},
    {"name": "Dr. House", "initials": "DH", "avatar": None},
]

SEEDS = [{'title': 'Как построить лунный парк?',
  'text': 'Ребята, у меня проблема с лунным парком. Не могу найти блэкджек, хотя всё делал по '
          'инструкции. Может кто-то уже сталкивался?',
  'tags': ['black-jack', 'bender']},
 {'title': 'Почему Bootstrap перебивает мои стили?',
  'text': 'Пишу в style.css цвет для кнопки, а он не применяется. Пришлось везде ставить '
          '!important, но говорят так нельзя. Что я делаю не так?',
  'tags': ['css', 'bootstrap']},
 {'title': 'Чем flexbox отличается от grid?',
  'text': 'Прошёл Flexbox Froggy, вроде понял flex. Но когда что лучше использовать, до сих пор '
          'непонятно. Можно на простом примере?',
  'tags': ['css', 'flexbox']},
 {'title': 'Не открывается localhost:8000 после runserver',
  'text': 'Запускаю python manage.py runserver, в консоли пишет что всё ок, а в браузере страница '
          'не грузится. Пробовал другой браузер, тоже самое.',
  'tags': ['python', 'django']},
 {'title': 'Как сделать, чтобы футер был всегда внизу?',
  'text': 'Когда на странице мало контента, футер поднимается к середине экрана и выглядит '
          'странно. Как прибить его к низу без position: fixed?',
  'tags': ['css', 'html']},
 {'title': 'Что такое box-sizing: border-box?',
  'text': 'В примерах постоянно вижу это свойство в самом начале css файла. Зачем оно нужно и что '
          'будет если его убрать?',
  'tags': ['css']},
 {'title': 'Как поднять nginx перед django?',
  'text': 'Хочу чтобы статику отдавал nginx, а всё остальное шло в gunicorn. Где почитать '
          'нормальный пример конфига?',
  'tags': ['nginx', 'django']}]

QUESTIONS = []
ANSWERS = {}
for number in range(1, 126):
    seed = SEEDS[(number - 1) % len(SEEDS)]
    answers = [
        {
            "id": index,
            "text": f"Ответ {index}. Сначала проверьте настройки и порядок подключения файлов. "
                    "В инструментах разработчика можно увидеть, какое правило применяется.",
            "author": USERS[index % len(USERS)],
            "rating": 40 - index,
            "correct": index == 1,
        }
        for index in range(1, 36)
    ]
    ANSWERS[number] = answers
    QUESTIONS.append({
        **seed,
        "id": number,
        "title": f"{seed['title']} · {number}",
        "author": USERS[number % len(USERS)],
        "rating": (number * 17) % 101,
        "answer_count": len(answers),
    })
