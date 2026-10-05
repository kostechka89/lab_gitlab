# Дима: Student Planner

Проект: [student-planner](http://gitlab.local:8080/devopsrabota2/student-planner). Исходники: [папка проекта](../gitlab-practice/project-2-student-planner/).
Последний pipeline в предоставленных доказательствах: [#7](http://gitlab.local:8080/devopsrabota2/student-planner/-/pipelines/7).

## Что делает приложение

Это планировщик заданий в браузере. Пользователь вводит предмет и задание, добавляет запись, отмечает выполнение и удаляет её.

## Как устроено

Planner хранит записи в словаре. render строит HTML; html.escape не даёт пользовательскому тексту стать HTML-разметкой. Handler принимает POST-формы, parse_qs разбирает поля. После изменения сервер отвечает 303 и возвращает пользователя на главную страницу. Данные остаются только в памяти.

Файлы: app.py — приложение; tests/test_app.py — автоматические тесты; tools.py — сборка, smoke и deploy; .gitlab-ci.yml — команды pipeline. Внешних библиотек, Telegram и платных API нет. Используется Python 3.12.

## Запуск перед защитой

Открой CMD в папке gitlab-practice\project-2-student-planner. Если на Windows доступен Python 3.12:

```bat
python --version
python -m pip install --no-index -r requirements.txt
python app.py --port 8002
```

Открой http://localhost:8002/. Введи Subject: DevOps, Assignment: Lab 2. Покажи Add assignment → Pending, complete → Completed, затем delete.

Если Python на хосте не установлен, из той же папки CMD запусти уже имеющийся Docker-образ:

```bat
docker run --rm -p 8002:8002 -v "%cd%:/app" -w /app python:3.12-slim python app.py --port 8002
```

Для серверов оставь терминал открытым; остановка — Ctrl+C. Приложение не запущено постоянно только потому, что deploy прошёл.

## Какие тесты реальные

Добавление, завершение и удаление; обязательные поля; экранирование <script> и A&B. Smoke отправляет настоящие HTTP-формы и проверяет HTML после каждого действия.
В этом проекте 3 unittest-теста. Команда:

```bat
python -m unittest discover -s tests -v
```

Unit-тесты проверяют функции, smoke — запуск программы из собранного пакета. Если проверяемый результат неверен, тест завершается ошибкой и job падает. `echo Tests passed` здесь не используется.

## Что показывать в GitLab

1. [Репозиторий](http://gitlab.local:8080/devopsrabota2/student-planner/-/tree/main): своё приложение и файлы.
2. [app.py](http://gitlab.local:8080/devopsrabota2/student-planner/-/blob/main/app.py): объясни логику в двух-трёх фразах.
3. [tests/test_app.py](http://gitlab.local:8080/devopsrabota2/student-planner/-/blob/main/tests/test_app.py): открой один тест и поясни assert.
4. [.gitlab-ci.yml](http://gitlab.local:8080/devopsrabota2/student-planner/-/blob/main/.gitlab-ci.yml): три stages и реальные команды.
5. [Pipeline #7](http://gitlab.local:8080/devopsrabota2/student-planner/-/pipelines/7): три зелёных jobs.
6. [Build](http://gitlab.local:8080/devopsrabota2/student-planner/-/jobs/19): компиляция app.py и сборка dist/application.zip.
7. [Test](http://gitlab.local:8080/devopsrabota2/student-planner/-/jobs/20): Ran 3 tests, OK и Application smoke: PASS.
8. [Deploy](http://gitlab.local:8080/devopsrabota2/student-planner/-/jobs/21): распаковка ZIP, повторная smoke-проверка, создание manifest.json.
9. [Artifacts](http://gitlab.local:8080/devopsrabota2/student-planner/-/jobs/21/artifacts/browse): deploy/app.py и контрольные суммы.

ZIP передаётся из build в test/deploy через artifacts и dependencies. Каждый job имеет отдельную файловую систему. Deploy учебный: подготовлен проверенный пакет, а не опубликован постоянный сервис.

## Короткий рассказ

«Мой индивидуальный проект — Student Planner. Это планировщик заданий в браузере. Пользователь вводит предмет и задание, добавляет запись, отмечает выполнение и удаляет её. В репозитории находятся приложение, тесты и CI-конфигурация. После push GitLab запускает pipeline. На build собирается ZIP, на test выполняются 3 автоматических теста и проверка запуска из ZIP, на deploy готовится папка с приложением и контрольными суммами. Вот pipeline и настоящие логи jobs».

## Если спросят

- Pipeline — вся последовательность проверки; stage — этап; job — задание с командами.
- Почему общий Runner? Общая инфраструктура разрешена; у приложений отдельные репозитории и результаты.
- Где зависимости? В requirements.txt указано, что сторонних пакетов нет; используется стандартная библиотека.
- Где deploy? В artifacts deploy_job. Это пакет файлов, а не production-сервер.
- Какой личный вклад? Назови только свои реальные действия. Назначение проекта участнику само по себе не доказывает, кто писал код.
