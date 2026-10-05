# Student Planner

Веб-приложение для учёта учебных заданий: предмет, название задания, завершение и удаление через формы.

Проект: http://gitlab.local:8080/devopsrabota2/student-planner

## Требования и установка

Python 3.12, стандартная библиотека. Сторонних зависимостей нет; requirements.txt содержит комментарий.

Из папки проекта, команды одинаковы для Windows CMD и PowerShell. Установленный Python 3.12 должен быть доступен как python. Если установлен Windows Python Launcher, создание venv можно выполнить через py -3.12.

```powershell
python --version
python -m venv .venv
.venv\Scripts\python.exe -m pip install --no-index -r requirements.txt
.venv\Scripts\python.exe app.py --port 8002
```

Активация venv не требуется. Примеры с `python` далее рассчитаны на Python 3.12; вместо него можно использовать `.venv\Scripts\python.exe`.

## Пример работы

Открыть http://localhost:8002/; в Subject ввести DevOps, в Assignment — Lab 2. Нажать Add assignment: появляется DevOps: Lab 2 — Pending. Кнопка complete меняет статус на Completed; delete удаляет строку.

## Основная логика

Класс Planner хранит задания в памяти. add проверяет заполненность предмета и задания; complete устанавливает done, delete удаляет запись. render собирает HTML и экранирует пользовательский текст через html.escape. Handler разбирает данные POST-форм через parse_qs и после изменения отвечает 303 с переходом на /. В интерфейсе статусы Pending и Completed.

Использованы: html.escape, http.server, urllib.parse.parse_qs, argparse.

Данные хранятся в памяти и исчезают после перезапуска. Приложение предназначено для доверенной учебной локальной среды. Остановить сервер: Ctrl+C.

## Структура

- app.py — приложение.
- tests/test_app.py — 3 unittest-теста.
- tools.py — build, smoke и учебный deploy.
- requirements.txt — объявление зависимостей.
- .gitlab-ci.yml — конфигурация CI.
- .gitignore — исключение venv, кешей и результатов сборки.

## Тестирование и сборка

```powershell
python -m pip install --no-index -r requirements.txt
python -m unittest discover -s tests -v
python tools.py build
python tools.py smoke dist/application.zip
python tools.py deploy
```

test_lifecycle проверяет добавление задания, Pending, переход в Completed и удаление; test_validation отклоняет пустые предмет и название; test_escape проверяет экранирование <script> и A&B. Тесты обнаруживают ошибки статуса, валидации и небезопасной вставки HTML. Smoke дополнительно проверяет HTTP-формы.

Smoke запускает сервер из ZIP на свободном порту, отправляет формы /add, /complete и /delete и проверяет текст HTML после каждой операции.

## CI и учебный deploy

В корне находится .gitlab-ci.yml с image: python:3.12-slim и последовательными stages build, test, deploy.

Перед каждым job: `python -m pip install --no-index -r requirements.txt`. Внешних зависимостей нет.

- build_job: `python tools.py build` компилирует app.py и собирает dist/application.zip с app.py, README.md, requirements.txt и имеющимися sample-файлами.
- test_job: `python -m unittest discover -s tests -v` и `python tools.py smoke dist/application.zip`.
- deploy_job: `python tools.py deploy` распаковывает ZIP в deploy/, выполняет smoke и записывает manifest.json с SHA256 файлов.

Каждый job работает в отдельном контейнере. test_job и deploy_job получают ZIP от build_job через artifacts и dependencies. Успешный test обязателен для перехода к deploy. Deployment — учебный пакет файлов, без постоянно работающего сервиса или публичного URL.

Для запуска пакета перейти в deploy и выполнить команду запуска из раздела установки.
