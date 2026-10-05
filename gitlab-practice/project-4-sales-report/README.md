# CSV Sales Report

Пакетная обработка CSV продаж и создание HTML-отчёта с выручкой по товарам и общей суммой.

Проект: http://gitlab.local:8080/devopsrabota2/sales-report

## Требования и установка

Python 3.12, стандартная библиотека. Сторонних зависимостей нет; requirements.txt содержит комментарий.

Из папки проекта, команды одинаковы для Windows CMD и PowerShell. Установленный Python 3.12 должен быть доступен как python. Если установлен Windows Python Launcher, создание venv можно выполнить через py -3.12.

```powershell
python --version
python -m venv .venv
.venv\Scripts\python.exe -m pip install --no-index -r requirements.txt
.venv\Scripts\python.exe app.py sample.csv --output report.html
```

Активация venv не требуется. Примеры с `python` далее рассчитаны на Python 3.12; вместо него можно использовать `.venv\Scripts\python.exe`.

## Пример работы

sample.csv содержит:
```csv
product,quantity,price
Book,2,10.10
Pen,3,1.50
```
После `python app.py sample.csv --output report.html` открыть report.html. Ожидаются Book: 20.20, Pen: 4.50, Total: 24.70. В PowerShell открыть файл командой `Start-Process .\report.html`, в CMD — `start "" report.html`.

## Основная логика

csv.DictReader требует заголовок product,quantity,price в таком порядке. summarize проверяет название, целое неотрицательное количество и конечную неотрицательную цену Decimal. Суммы quantity × price накапливаются по товарам. render сортирует товары, экранирует названия и форматирует суммы с двумя знаками. main сохраняет UTF-8 HTML; неверный файл или строка дают код 2.

Использованы: argparse, csv, decimal.Decimal, decimal.InvalidOperation, html.escape, pathlib.Path.

## Структура

- app.py — приложение.
- tests/test_app.py — 4 unittest-теста.
- tools.py — build, smoke и учебный deploy.
- requirements.txt — объявление зависимостей.
- .gitlab-ci.yml — конфигурация CI.
- .gitignore — исключение venv, кешей и результатов сборки.
- sample.csv — пример входных продаж.

## Тестирование и сборка

```powershell
python -m pip install --no-index -r requirements.txt
python -m unittest discover -s tests -v
python tools.py build
python tools.py smoke dist/application.zip
python tools.py deploy
```

test_aggregation проверяет накопление нескольких строк одного товара и Total: 26.70 для тестового набора; test_invalid отклоняет отрицательные числа, NaN, нецелое количество и пустой товар; test_header проверяет заголовок; test_empty_and_escape проверяет пустой CSV и HTML-экранирование. Эти тесты обнаруживают ошибки расчётов и обработки входа. В sample.csv другой набор: его итог 24.70.

Smoke запускает CLI из ZIP с sample.csv, создаёт HTML во временной папке и проверяет Total: 24.70.

## CI и учебный deploy

В корне находится .gitlab-ci.yml с image: python:3.12-slim и последовательными stages build, test, deploy.

Перед каждым job: `python -m pip install --no-index -r requirements.txt`. Внешних зависимостей нет.

- build_job: `python tools.py build` компилирует app.py и собирает dist/application.zip с app.py, README.md, requirements.txt и имеющимися sample-файлами.
- test_job: `python -m unittest discover -s tests -v` и `python tools.py smoke dist/application.zip`.
- deploy_job: `python tools.py deploy` распаковывает ZIP в deploy/, выполняет smoke и записывает manifest.json с SHA256 файлов.

Каждый job работает в отдельном контейнере. test_job и deploy_job получают ZIP от build_job через artifacts и dependencies. Успешный test обязателен для перехода к deploy. Deployment — учебный пакет файлов, без постоянно работающего сервиса или публичного URL.

Для запуска пакета перейти в deploy и выполнить команду запуска из раздела установки.
