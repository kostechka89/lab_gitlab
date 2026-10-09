# Показ на компьютере Кости

Этот сценарий идёт в том же порядке, что TEAM-SPEECH.md. Здесь указано, что открыть и показать. Исторические IDs соответствуют успешным pipeline из предоставленных доказательств; не выдавай их за новые запуски.

## Перед проверкой — Костя

1. Запусти Docker Desktop и дождись готовности Engine.
2. Открой CMD и выполни:

```bat
cd /d C:\Users\kokstik\lab_gitlab-main\gitlab-practice\infrastructure
docker info
docker compose up -d --pull never gitlab runner
docker compose ps
curl.exe --noproxy "*" -I http://gitlab.local:8080
docker compose exec runner gitlab-runner verify
```

Дождись ответа сайта. 302 на страницу входа — нормально. Verify проверяет регистрацию; Online проверь в интерфейсе.

3. Открой Chrome для GitLab:

```bat
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="%LOCALAPPDATA%\GitLabChrome" --no-proxy-server --disable-extensions "http://gitlab.local:8080/devopsrabota2"
```

Войди, если требуется. Пароль и токены не показывай при демонстрации экрана.

4. Подготовь вкладки группы, Runner и четырёх pipeline. Открой Word-отчёт при необходимости. Не удаляй volumes и не обновляй образы перед проверкой.
5. Команды приложений ниже предполагают доступный Python 3.12. Если Python на Windows не установлен, используй Docker-команды из индивидуальных файлов участников. Проверь запуск заранее.

## 1. Начало — Костя показывает свою настройку

Открой [группу](http://gitlab.local:8080/devopsrabota2): должны быть четыре отдельных проекта.
Открой [Runner](http://gitlab.local:8080/admin/runners): покажи devops-docker и Online.
Открой на диске infrastructure/compose.yaml и покажи:

- два сервиса gitlab и runner;
- external_url и проброс 8080:8080;
- внутренний Puma 8081;
- volumes для постоянных данных;
- общую сеть gitlab-practice-net;
- Docker socket у Runner.

Скажи: «Это конфигурация среды, которую я запускал на своём ПК. Регистрацию Runner мы сейчас подтверждаем его статусом и настройками, а не повторяем с показом токена».

## 2. Todo API — Костя

В отдельном CMD:

```bat
cd /d C:\Users\kokstik\lab_gitlab-main\gitlab-practice\project-1-todo-api
python app.py --port 8001
```

Оставь окно работающим. Во втором окне **PowerShell**:

```powershell
$t = Invoke-RestMethod http://localhost:8001/tasks -Method Post -ContentType application/json -Body '{"title":"Prepare lab"}'
$t
Invoke-RestMethod http://localhost:8001/tasks
Invoke-RestMethod ("http://localhost:8001/tasks/"+$t.id) -Method Patch
Invoke-RestMethod ("http://localhost:8001/tasks/"+$t.id) -Method Delete
Invoke-RestMethod http://localhost:8001/tasks
```

Покажи изменение done и удаление. Пустой итоговый список получится, если других задач нет.
Затем открой в GitLab:

- [исходник](http://gitlab.local:8080/devopsrabota2/todo-api/-/blob/main/app.py);
- [тесты](http://gitlab.local:8080/devopsrabota2/todo-api/-/blob/main/tests/test_app.py);
- [YAML](http://gitlab.local:8080/devopsrabota2/todo-api/-/blob/main/.gitlab-ci.yml);
- [pipeline #6](http://gitlab.local:8080/devopsrabota2/todo-api/-/pipelines/6);
- [build #16](http://gitlab.local:8080/devopsrabota2/todo-api/-/jobs/16);
- [test #17](http://gitlab.local:8080/devopsrabota2/todo-api/-/jobs/17);
- [deploy #18](http://gitlab.local:8080/devopsrabota2/todo-api/-/jobs/18);
- [deploy artifacts](http://gitlab.local:8080/devopsrabota2/todo-api/-/jobs/18/artifacts/browse).

В test покажи Ran 4 tests, OK и smoke PASS. В deploy — реальную команду, успешное завершение и app.py/manifest.json в artifact. На этой части подробно объясни общий CI; дальше не нужно повторять всё слово в слово.

## 3. Planner — Дима говорит, Костя переключает окна

В новом CMD:

```bat
cd /d C:\Users\kokstik\lab_gitlab-main\gitlab-practice\project-2-student-planner
python app.py --port 8002
```

Открой http://localhost:8002/ в Chrome без прокси. Добавь DevOps / Lab 2, нажми complete, затем delete.

Покажи [тесты](http://gitlab.local:8080/devopsrabota2/student-planner/-/blob/main/tests/test_app.py), [pipeline #7](http://gitlab.local:8080/devopsrabota2/student-planner/-/pipelines/7) и [test #20](http://gitlab.local:8080/devopsrabota2/student-planner/-/jobs/20). Найди Ran 3 tests и OK. При вопросе о build/deploy открой соответствующие jobs прямо из pipeline.

## 4. Sales Report — Лариса говорит, Костя показывает

В новом CMD:

```bat
cd /d C:\Users\kokstik\lab_gitlab-main\gitlab-practice\project-4-sales-report
type sample.csv
python app.py sample.csv --output report.html
start "" report.html
```

Покажи CSV, команду и HTML: Book 20.20, Pen 4.50, Total 24.70.
Открой [тесты](http://gitlab.local:8080/devopsrabota2/sales-report/-/blob/main/tests/test_app.py), [pipeline #9](http://gitlab.local:8080/devopsrabota2/sales-report/-/pipelines/9) и [test #26](http://gitlab.local:8080/devopsrabota2/sales-report/-/jobs/26). Покажи Ran 4 tests, OK и smoke.

## 5. Text Analyzer — Настя говорит, Костя показывает

В новом CMD:

```bat
cd /d C:\Users\kokstik\lab_gitlab-main\gitlab-practice\project-3-text-analyzer
type sample.txt
python app.py sample.txt
echo Hello hello world| python app.py
```

Покажи words=3 и unique_words=2. Characters могут отличаться при разных переводах строк; не сравнивай это поле с придуманным числом.
Открой [тесты](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/blob/main/tests/test_app.py), [pipeline #8](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/pipelines/8) и [test #23](http://gitlab.local:8080/devopsrabota2/text-analyzer/-/jobs/23). Покажи Ran 4 tests и OK.

## 6. Завершение — Костя

Вернись на страницу группы. По запросу преподавателя можно запустить новый pipeline: проект → Build → Pipelines → New pipeline / Run pipeline → main. Не утверждай, что новый запуск прошёл, пока jobs не завершились.

Если спросят о тестах, можно дополнительно выполнить в папке любого приложения:

```bat
python -m unittest discover -s tests -v
```

Но основное доказательство CI — реальные логи test_job, а не только локальная команда.

## После показа

Останови серверы приложений через Ctrl+C. Если среда больше не нужна сейчас:

```bat
cd /d C:\Users\kokstik\lab_gitlab-main\gitlab-practice\infrastructure
docker compose stop
```

Данные останутся. Ссылки gitlab.local предназначены для этого ПК; для демонстрации из другого места используй свой ПК/демонстрацию экрана либо заранее настрой доступ к серверу.
