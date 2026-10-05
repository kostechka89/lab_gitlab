# Настя: Text Analyzer CLI

Проект: [text-analyzer](http://gitlab.local:8080/devopsrabota2/text-analyzer). Исходники: [папка проекта](../gitlab-practice/project-3-text-analyzer/).
Последний pipeline в предоставленных доказательствах: [#8](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/pipelines/8).

## Что делает приложение

Консольная программа считает символы, строки, слова, уникальные слова и пять самых частых слов. Результат выводится в JSON.

## Как устроено

Path читает UTF-8 файл. analyze приводит текст к нижнему регистру, регулярное выражение выделяет слова, set считает уникальные слова, Counter — частоты. Без имени файла программа читает stdin. Ошибка чтения возвращает код 2.

Файлы: app.py — приложение; tests/test_app.py — автоматические тесты; tools.py — сборка, smoke и deploy; .gitlab-ci.yml — команды pipeline. Внешних библиотек, Telegram и платных API нет. Используется Python 3.12.

## Запуск перед защитой

Открой CMD в папке gitlab-practice\project-3-text-analyzer. Если на Windows доступен Python 3.12:

```bat
python --version
python -m pip install --no-index -r requirements.txt
python app.py sample.txt
```

Покажи sample.txt и результат команды: words=3, unique_words=2. Затем в CMD: `echo Hello hello world| python app.py`. Объясни, что регистр не влияет на уникальные слова, а пробелы и переводы строк входят в characters.

Если Python на хосте не установлен, из той же папки CMD запусти уже имеющийся Docker-образ:

```bat
docker run --rm -v "%cd%:/app" -w /app python:3.12-slim python app.py sample.txt
```

Для серверов оставь терминал открытым; остановка — Ctrl+C. Приложение не запущено постоянно только потому, что deploy прошёл.

## Какие тесты реальные

Количество слов, строк и символов; повторяющиеся слова; пустой текст; русский текст и пунктуация. Smoke запускает CLI с файлом и со стандартным вводом и проверяет JSON.
В этом проекте 4 unittest-теста. Команда:

```bat
python -m unittest discover -s tests -v
```

Unit-тесты проверяют функции, smoke — запуск программы из собранного пакета. Если проверяемый результат неверен, тест завершается ошибкой и job падает. `echo Tests passed` здесь не используется.

## Что показывать в GitLab

1. [Репозиторий](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/tree/main): своё приложение и файлы.
2. [app.py](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/blob/main/app.py): объясни логику в двух-трёх фразах.
3. [tests/test_app.py](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/blob/main/tests/test_app.py): открой один тест и поясни assert.
4. [.gitlab-ci.yml](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/blob/main/.gitlab-ci.yml): три stages и реальные команды.
5. [Pipeline #8](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/pipelines/8): три зелёных jobs.
6. [Build](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/jobs/22): компиляция app.py и сборка dist/application.zip.
7. [Test](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/jobs/23): Ran 4 tests, OK и Application smoke: PASS.
8. [Deploy](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/jobs/24): распаковка ZIP, повторная smoke-проверка, создание manifest.json.
9. [Artifacts](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/jobs/24/artifacts/browse): deploy/app.py и контрольные суммы.

ZIP передаётся из build в test/deploy через artifacts и dependencies. Каждый job имеет отдельную файловую систему. Deploy учебный: подготовлен проверенный пакет, а не опубликован постоянный сервис.

## Короткий рассказ

«Мой индивидуальный проект — Text Analyzer CLI. Консольная программа считает символы, строки, слова, уникальные слова и пять самых частых слов. Результат выводится в JSON. В репозитории находятся приложение, тесты и CI-конфигурация. После push GitLab запускает pipeline. На build собирается ZIP, на test выполняются 4 автоматических теста и проверка запуска из ZIP, на deploy готовится папка с приложением и контрольными суммами. Вот pipeline и настоящие логи jobs».

## Если спросят

- Pipeline — вся последовательность проверки; stage — этап; job — задание с командами.
- Почему общий Runner? Общая инфраструктура разрешена; у приложений отдельные репозитории и результаты.
- Где зависимости? В requirements.txt указано, что сторонних пакетов нет; используется стандартная библиотека.
- Где deploy? В artifacts deploy_job. Это пакет файлов, а не production-сервер.
- Какой личный вклад? Назови только свои реальные действия. Назначение проекта участнику само по себе не доказывает, кто писал код.
