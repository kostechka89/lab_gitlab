# Todo REST API

HTTP API для управления задачами: создание, просмотр списка, завершение и удаление.

Проект: http://gitlab.local:8080/devopsrabota2/todo-api

## Требования и установка

Python 3.12, стандартная библиотека. Сторонних зависимостей нет; requirements.txt содержит комментарий.

Из папки проекта, команды одинаковы для Windows CMD и PowerShell. Установленный Python 3.12 должен быть доступен как python. Если установлен Windows Python Launcher, создание venv можно выполнить через py -3.12.

```powershell
python --version
python -m venv .venv
.venv\Scripts\python.exe -m pip install --no-index -r requirements.txt
.venv\Scripts\python.exe app.py --port 8001
```

Активация venv не требуется. Примеры с `python` далее рассчитаны на Python 3.12; вместо него можно использовать `.venv\Scripts\python.exe`.

## Пример работы

В одном окне запустить сервер, в другом PowerShell выполнить:
```powershell
$item = Invoke-RestMethod -Uri http://localhost:8001/tasks -Method Post -ContentType application/json -Body '{"title":"Learn Git"}'
Invoke-RestMethod -Uri http://localhost:8001/tasks
Invoke-RestMethod -Uri ("http://localhost:8001/tasks/"+$item.id) -Method Patch
Invoke-RestMethod -Uri ("http://localhost:8001/tasks/"+$item.id) -Method Delete
Invoke-RestMethod -Uri http://localhost:8001/tasks
```
На свежем сервере создаётся задача id=1, title=Learn Git, done=False; PATCH возвращает done=True, DELETE возвращает deleted=1, итоговый список пуст.

## Основная логика

Класс Tasks хранит задачи в словаре по целочисленному ID. add проверяет непустую строку, удаляет пробелы по краям и увеличивает next_id. complete меняет done на True, delete удаляет запись. Handler преобразует HTTP-запросы в вызовы Tasks и формирует JSON с кодами 200, 201, 400 или 404. ThreadingHTTPServer обслуживает запросы.

Использованы: json, http.server, argparse.

Данные хранятся в памяти и исчезают после перезапуска. Приложение предназначено для доверенной учебной локальной среды. Остановить сервер: Ctrl+C.

## Структура

- app.py — приложение.
- tests/test_app.py — 4 unittest-теста.
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

test_lifecycle проверяет создание, нормализацию названия, завершение и удаление; test_validation отклоняет пустую строку, пробелы, None и число; test_unique_ids обнаруживает повтор ID; test_missing проверяет KeyError для отсутствующей задачи. Unit-тесты проверяют модель Tasks; HTTP-поведение дополнительно проверяет smoke.

Smoke запускает HTTP-сервер на свободном локальном порту из распакованного ZIP и проверяет POST, GET, PATCH, DELETE и пустой итоговый список.

## CI и учебный deploy

В корне находится .gitlab-ci.yml с image: python:3.12-slim и последовательными stages build, test, deploy.

Перед каждым job: `python -m pip install --no-index -r requirements.txt`. Внешних зависимостей нет.

- build_job: `python tools.py build` компилирует app.py и собирает dist/application.zip с app.py, README.md, requirements.txt и имеющимися sample-файлами.
- test_job: `python -m unittest discover -s tests -v` и `python tools.py smoke dist/application.zip`.
- deploy_job: `python tools.py deploy` распаковывает ZIP в deploy/, выполняет smoke и записывает manifest.json с SHA256 файлов.

Каждый job работает в отдельном контейнере. test_job и deploy_job получают ZIP от build_job через artifacts и dependencies. Успешный test обязателен для перехода к deploy. Deployment — учебный пакет файлов, без постоянно работающего сервиса или публичного URL.

Для запуска пакета перейти в deploy и выполнить команду запуска из раздела установки.
