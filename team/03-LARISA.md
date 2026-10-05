# Лариса: CSV Sales Report

Проект: [sales-report](http://gitlab.local:8080/devopsrabota2/sales-report). Исходники: [папка проекта](../gitlab-practice/project-4-sales-report/).
Последний pipeline в предоставленных доказательствах: [#9](http://gitlab.local:8080/devopsrabota2/sales-report/-/pipelines/9).

## Что делает приложение

Программа читает продажи из CSV и создаёт HTML-отчёт: выручка по каждому товару и общий итог.

## Как устроено

csv.DictReader читает строки. Для каждой продажи вычисляется quantity × price, суммы объединяются по названию товара. Decimal используется для точных денежных расчётов. Проверяются заголовок CSV, название, количество и цена. Названия экранируются перед вставкой в HTML.

Файлы: app.py — приложение; tests/test_app.py — автоматические тесты; tools.py — сборка, smoke и deploy; .gitlab-ci.yml — команды pipeline. Внешних библиотек, Telegram и платных API нет. Используется Python 3.12.

## Запуск перед защитой

Открой CMD в папке gitlab-practice\project-4-sales-report. Если на Windows доступен Python 3.12:

```bat
python --version
python -m pip install --no-index -r requirements.txt
python app.py sample.csv --output report.html
```

Сначала открой sample.csv: заголовок product,quantity,price. После команды открой report.html двойным щелчком. Покажи Book: 20.20, Pen: 4.50, Total: 24.70. Цены записываются с точкой.

Если Python на хосте не установлен, из той же папки CMD запусти уже имеющийся Docker-образ:

```bat
docker run --rm -v "%cd%:/app" -w /app python:3.12-slim python app.py sample.csv --output report.html
```

Для серверов оставь терминал открытым; остановка — Ctrl+C. Приложение не запущено постоянно только потому, что deploy прошёл.

## Какие тесты реальные

Суммирование повторяющихся товаров, итог, неверный заголовок, отрицательные и некорректные значения, пустой CSV и экранирование HTML. Smoke создаёт настоящий отчёт и проверяет итог 24.70.
В этом проекте 4 unittest-теста. Команда:

```bat
python -m unittest discover -s tests -v
```

Unit-тесты проверяют функции, smoke — запуск программы из собранного пакета. Если проверяемый результат неверен, тест завершается ошибкой и job падает. `echo Tests passed` здесь не используется.

## Что показывать в GitLab

1. [Репозиторий](http://gitlab.local:8080/devopsrabota2/sales-report/-/tree/main): своё приложение и файлы.
2. [app.py](http://gitlab.local:8080/devopsrabota2/sales-report/-/blob/main/app.py): объясни логику в двух-трёх фразах.
3. [tests/test_app.py](http://gitlab.local:8080/devopsrabota2/sales-report/-/blob/main/tests/test_app.py): открой один тест и поясни assert.
4. [.gitlab-ci.yml](http://gitlab.local:8080/devopsrabota2/sales-report/-/blob/main/.gitlab-ci.yml): три stages и реальные команды.
5. [Pipeline #9](http://gitlab.local:8080/devopsrabota2/sales-report/-/pipelines/9): три зелёных jobs.
6. [Build](http://gitlab.local:8080/devopsrabota2/sales-report/-/jobs/25): компиляция app.py и сборка dist/application.zip.
7. [Test](http://gitlab.local:8080/devopsrabota2/sales-report/-/jobs/26): Ran 4 tests, OK и Application smoke: PASS.
8. [Deploy](http://gitlab.local:8080/devopsrabota2/sales-report/-/jobs/27): распаковка ZIP, повторная smoke-проверка, создание manifest.json.
9. [Artifacts](http://gitlab.local:8080/devopsrabota2/sales-report/-/jobs/27/artifacts/browse): deploy/app.py и контрольные суммы.

ZIP передаётся из build в test/deploy через artifacts и dependencies. Каждый job имеет отдельную файловую систему. Deploy учебный: подготовлен проверенный пакет, а не опубликован постоянный сервис.

## Короткий рассказ

«Мой индивидуальный проект — CSV Sales Report. Программа читает продажи из CSV и создаёт HTML-отчёт: выручка по каждому товару и общий итог. В репозитории находятся приложение, тесты и CI-конфигурация. После push GitLab запускает pipeline. На build собирается ZIP, на test выполняются 4 автоматических теста и проверка запуска из ZIP, на deploy готовится папка с приложением и контрольными суммами. Вот pipeline и настоящие логи jobs».

## Если спросят

- Pipeline — вся последовательность проверки; stage — этап; job — задание с командами.
- Почему общий Runner? Общая инфраструктура разрешена; у приложений отдельные репозитории и результаты.
- Где зависимости? В requirements.txt указано, что сторонних пакетов нет; используется стандартная библиотека.
- Где deploy? В artifacts deploy_job. Это пакет файлов, а не production-сервер.
- Какой личный вклад? Назови только свои реальные действия. Назначение проекта участнику само по себе не доказывает, кто писал код.
