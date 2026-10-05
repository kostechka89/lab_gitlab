# Костя: Todo REST API

Проект: [todo-api](http://gitlab.local:8080/devopsrabota2/todo-api). Исходники: [папка проекта](../gitlab-practice/project-1-todo-api/).
Последний pipeline в предоставленных доказательствах: [#6](http://gitlab.local:8080/devopsrabota2/todo-api/-/pipelines/6).

## Общая часть: что говорит Костя

«Я настраивал общую среду на своём Windows-компьютере: установил и запустил GitLab и Runner через Docker Compose, создал группу и загрузил четыре проекта. Для каждого приложения у нас отдельный репозиторий и pipeline. То, что сервер один, не объединяет приложения в один проект».

Не говори, что остальные самостоятельно написали весь код, если это не соответствует фактам. Нейтральная фраза: «Индивидуальные проекты распределены между участниками; загрузку и настройку общего сервера я выполнял централизованно».

GitLab — сервер репозиториев и координатор pipeline. Runner получает задания и выполняет их. Docker executor запускает каждый job в отдельном контейнере Python. Runner один, проектов четыре. Он обрабатывает jobs по очереди.

В Compose сайт опубликован как 8080:8080, SSH — 2222:22. Puma использует внутренний порт 8081, чтобы не конфликтовать с nginx. Volumes сохраняют данные при перезапуске. Сеть gitlab-practice-net позволяет Runner и контейнерам jobs обращаться к gitlab.local.

## Что делает приложение

Задачи доступны по HTTP. POST /tasks создаёт задачу, GET /tasks возвращает список, PATCH /tasks/ID отмечает выполнение, DELETE /tasks/ID удаляет задачу. Ответы передаются в JSON.

## Как устроено

В app.py класс Tasks хранит словарь задач и следующий ID. Класс Handler разбирает HTTP-запрос и вызывает нужный метод Tasks. Пустое название даёт 400, отсутствующая задача — 404. После перезапуска данные исчезают: базы данных здесь нет.

Файлы: app.py — приложение; tests/test_app.py — автоматические тесты; tools.py — сборка, smoke и deploy; .gitlab-ci.yml — команды pipeline. Внешних библиотек, Telegram и платных API нет. Используется Python 3.12.

## Запуск перед защитой

Открой CMD в папке gitlab-practice\project-1-todo-api. Если на Windows доступен Python 3.12:

```bat
python --version
python -m pip install --no-index -r requirements.txt
python app.py --port 8001
```

В PowerShell во втором окне:
```powershell
$t = Invoke-RestMethod http://localhost:8001/tasks -Method Post -ContentType application/json -Body '{"title":"Prepare lab"}'
Invoke-RestMethod http://localhost:8001/tasks
Invoke-RestMethod ("http://localhost:8001/tasks/"+$t.id) -Method Patch
Invoke-RestMethod ("http://localhost:8001/tasks/"+$t.id) -Method Delete
```
ID берём из ответа, а не предполагаем, что он всегда равен 1.

Если Python на хосте не установлен, из той же папки CMD запусти уже имеющийся Docker-образ:

```bat
docker run --rm -p 8001:8001 -v "%cd%:/app" -w /app python:3.12-slim python app.py --port 8001
```

Для серверов оставь терминал открытым; остановка — Ctrl+C. Приложение не запущено постоянно только потому, что deploy прошёл.

## Какие тесты реальные

Жизненный цикл задачи, непустое название, разные ID и обращение к отсутствующей задаче. HTTP отдельно проверяется smoke: сервер запускается из ZIP, к нему отправляются реальные запросы.
В этом проекте 4 unittest-теста. Команда:

```bat
python -m unittest discover -s tests -v
```

Unit-тесты проверяют функции, smoke — запуск программы из собранного пакета. Если проверяемый результат неверен, тест завершается ошибкой и job падает. `echo Tests passed` здесь не используется.

## Что показывать в GitLab

1. [Репозиторий](http://gitlab.local:8080/devopsrabota2/todo-api/-/tree/main): своё приложение и файлы.
2. [app.py](http://gitlab.local:8080/devopsrabota2/todo-api/-/blob/main/app.py): объясни логику в двух-трёх фразах.
3. [tests/test_app.py](http://gitlab.local:8080/devopsrabota2/todo-api/-/blob/main/tests/test_app.py): открой один тест и поясни assert.
4. [.gitlab-ci.yml](http://gitlab.local:8080/devopsrabota2/todo-api/-/blob/main/.gitlab-ci.yml): три stages и реальные команды.
5. [Pipeline #6](http://gitlab.local:8080/devopsrabota2/todo-api/-/pipelines/6): три зелёных jobs.
6. [Build](http://gitlab.local:8080/devopsrabota2/todo-api/-/jobs/16): компиляция app.py и сборка dist/application.zip.
7. [Test](http://gitlab.local:8080/devopsrabota2/todo-api/-/jobs/17): Ran 4 tests, OK и Application smoke: PASS.
8. [Deploy](http://gitlab.local:8080/devopsrabota2/todo-api/-/jobs/18): распаковка ZIP, повторная smoke-проверка, создание manifest.json.
9. [Artifacts](http://gitlab.local:8080/devopsrabota2/todo-api/-/jobs/18/artifacts/browse): deploy/app.py и контрольные суммы.

ZIP передаётся из build в test/deploy через artifacts и dependencies. Каждый job имеет отдельную файловую систему. Deploy учебный: подготовлен проверенный пакет, а не опубликован постоянный сервис.

## Короткий рассказ

«Мой индивидуальный проект — Todo REST API. Задачи доступны по HTTP. POST /tasks создаёт задачу, GET /tasks возвращает список, PATCH /tasks/ID отмечает выполнение, DELETE /tasks/ID удаляет задачу. Ответы передаются в JSON. В репозитории находятся приложение, тесты и CI-конфигурация. После push GitLab запускает pipeline. На build собирается ZIP, на test выполняются 4 автоматических теста и проверка запуска из ZIP, на deploy готовится папка с приложением и контрольными суммами. Вот pipeline и настоящие логи jobs».

## Если спросят

- Pipeline — вся последовательность проверки; stage — этап; job — задание с командами.
- Почему общий Runner? Общая инфраструктура разрешена; у приложений отдельные репозитории и результаты.
- Где зависимости? В requirements.txt указано, что сторонних пакетов нет; используется стандартная библиотека.
- Где deploy? В artifacts deploy_job. Это пакет файлов, а не production-сервер.
- Какой личный вклад? Назови только свои реальные действия. Назначение проекта участнику само по себе не доказывает, кто писал код.
