# Text Analyzer CLI

Консольный анализ UTF-8 текста из файла или stdin: символы, строки, слова, уникальные слова и пять наиболее частых слов.

Проект: http://gitlab.local:8080/devopsrabota2/text-analyzer

## Требования и установка

Python 3.12, стандартная библиотека. Сторонних зависимостей нет; requirements.txt содержит комментарий.

Из папки проекта, команды одинаковы для Windows CMD и PowerShell. Установленный Python 3.12 должен быть доступен как python. Если установлен Windows Python Launcher, создание venv можно выполнить через py -3.12.

```powershell
python --version
python -m venv .venv
.venv\Scripts\python.exe -m pip install --no-index -r requirements.txt
.venv\Scripts\python.exe app.py sample.txt
```

Активация venv не требуется. Примеры с `python` далее рассчитаны на Python 3.12; вместо него можно использовать `.venv\Scripts\python.exe`.

## Пример работы

Команда `python app.py sample.txt` анализирует файл Hello hello! и World на следующей строке. Для сохранённого sample.txt ожидаются characters=19 (включая завершающий перевод строки), lines=2, words=3, unique_words=2, top_words=[["hello",2],["world",1]].

В CMD можно проверить stdin:
```cmd
echo one two| python app.py
```
Ожидается words=2 и unique_words=2; количество символов учитывает перевод строки, добавленный echo.

## Основная логика

analyze приводит текст к нижнему регистру и выделяет слова регулярным выражением с поддержкой Unicode и внутренних апострофов/дефисов. len(text) считает символы, splitlines — строки, set — уникальные слова, Counter.most_common(5) — частоты. main читает UTF-8 файл или stdin и печатает JSON. Ошибка чтения завершает CLI с кодом 2.

Использованы: argparse, json, re, sys, collections.Counter, pathlib.Path.

## Структура

- app.py — приложение.
- tests/test_app.py — 4 unittest-теста.
- tools.py — build, smoke и учебный deploy.
- requirements.txt — объявление зависимостей.
- .gitlab-ci.yml — конфигурация CI.
- .gitignore — исключение venv, кешей и результатов сборки.
- sample.txt — пример UTF-8 текста.

## Тестирование и сборка

```powershell
python -m pip install --no-index -r requirements.txt
python -m unittest discover -s tests -v
python tools.py build
python tools.py smoke dist/application.zip
python tools.py deploy
```

test_counts проверяет числа и частоту hello для Hello hello!\nWorld; test_empty проверяет пустой ввод; test_unicode проверяет регистронезависимость кириллицы; test_punctuation проверяет слово one-two и пунктуацию. Тесты обнаруживают неверный подсчёт, неправильную обработку регистра, пустого текста и дефиса.

Smoke запускает CLI из ZIP с sample.txt и проверяет words=3; второй запуск передаёт one two через stdin и проверяет words=2.

## CI и учебный deploy

В корне находится .gitlab-ci.yml с image: python:3.12-slim и последовательными stages build, test, deploy.

Перед каждым job: `python -m pip install --no-index -r requirements.txt`. Внешних зависимостей нет.

- build_job: `python tools.py build` компилирует app.py и собирает dist/application.zip с app.py, README.md, requirements.txt и имеющимися sample-файлами.
- test_job: `python -m unittest discover -s tests -v` и `python tools.py smoke dist/application.zip`.
- deploy_job: `python tools.py deploy` распаковывает ZIP в deploy/, выполняет smoke и записывает manifest.json с SHA256 файлов.

Каждый job работает в отдельном контейнере. test_job и deploy_job получают ZIP от build_job через artifacts и dependencies. Успешный test обязателен для перехода к deploy. Deployment — учебный пакет файлов, без постоянно работающего сервиса или публичного URL.

Для запуска пакета перейти в deploy и выполнить команду запуска из раздела установки.
