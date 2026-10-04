# Практическая работа №2 — пошаговый маршрут

## Что уже готово

Четыре папки project-* — четыре независимых будущих репозитория. Не выполняйте git init в корне комплекта.
Локальные команды реально проверены: см. LOCAL-VERIFICATION.txt. GitLab, Runner и pipeline этим логом не подтверждены.
Deploy — подготовка проверенного пакета deploy/ с SHA256-манифестом, без постоянно работающего production-сервиса.

## Шаг 1. Подготовить компьютер

Дальнейшие команды выполняйте на своём компьютере, где будете открывать браузер, в Bash (Linux/macOS или WSL2).
Установите Git и Docker с Compose v2. На Windows используйте Docker Desktop с интеграцией WSL2 и храните комплект в файловой системе WSL.
Выделите Docker минимум 8 ГБ RAM, желательно 4 CPU и 15–20 ГБ свободного диска для учебной среды.
Проверьте:

```bash
git --version
docker version
docker compose version
```

Скачайте и распакуйте gitlab-practice.zip. Перейдите в распакованную папку gitlab-practice.

Добавьте строку в hosts компьютера, на котором работает браузер:

```text
127.0.0.1 gitlab.local
```

Linux/macOS: `sudo nano /etc/hosts`, добавьте строку, сохраните.
Windows: запустите Блокнот от администратора, откройте `C:\Windows\System32\drivers\etc\hosts` (тип файлов «Все файлы»), добавьте строку и сохраните. В WSL при необходимости добавьте строку и в `/etc/hosts`.
`gitlab.local` — выбранное имя нашей установки, а не адрес существующего чужого сервера.

## Шаг 2. Запустить GitLab

```bash
cd infrastructure
docker compose up -d gitlab
docker compose ps
docker compose logs --tail=100 gitlab
```

Первый запуск может занять несколько минут. Откройте в браузере [локальный GitLab](http://gitlab.local:8080).
Если видите 502, дождитесь готовности; проверяйте `docker compose logs --tail=100 gitlab`. Если контейнер перезапускается, прочитайте его ошибки и проверьте RAM/свободное место. Если порт занят, освободите его; изменение порта требует согласованного изменения external_url и ports.

Compose использует `latest`, поэтому конкретная версия определяется скачанным образом. Для воспроизводимости после скачивания запишите версии и digest:

```bash
docker compose exec gitlab gitlab-rake gitlab:env:info
docker image inspect gitlab/gitlab-ce:latest --format '{{json .RepoDigests}}'
```

Не обновляйте образы в середине работы. Compose здесь подготовлен, но запуск этого стека в текущей облачной среде не проверялся.

## Шаг 3. Первый вход

Получите фактический начальный пароль:

```bash
docker compose exec gitlab cat /etc/gitlab/initial_root_password
```

Войдите: username `root`, password — значение из файла. Не публикуйте пароль или токены в отчёте.
Файл начального пароля удаляется при последующем reconfigure после 24 часов; если он уже отсутствует и пароль потерян:

```bash
docker compose exec gitlab gitlab-rake 'gitlab:password:reset[root]'
```

Задайте новый пароль по запросам команды. В интерфейсе профиль → Edit profile / Preferences → Password смените начальный пароль, если это ещё не сделано.

## Шаг 4. Создать группу и пользователей

Для простой групповой работы root может создать все четыре проекта. Чтобы у студентов были отдельные учётные записи:

1. Откройте Admin → Overview → Users → New user.
2. Введите имя, уникальный username и реальный email каждого студента. Повторите четыре раза.
3. Если локальная установка не отправляет почту, не ждите письма: откройте пользователя в Admin → Users → Edit и задайте пароль; если требуется подтверждение email, используйте Confirm user. Передайте пароль соответствующему студенту вне отчёта.
4. Откройте Groups → New group → Create group. Назовите группу `practice-2`; задайте Visibility: Private.
5. В группе откройте Manage → Members → Invite members. Добавьте студентов с ролью Maintainer для учебной группы.

В разных версиях названия меню могут немного отличаться. Если пункт отсутствует, зафиксируйте версию и фактический экран, прежде чем менять настройку наугад.

## Шаг 5. Создать общий Runner

В терминале, всё ещё в infrastructure:

```bash
docker compose up -d runner
```

В браузере под root откройте Admin → CI/CD → Runners → Create instance runner / New instance runner.
Выберите Linux; включите **Run untagged jobs**. Теги оставьте пустыми. Для лабораторной не включайте **Protected**: main у новых проектов может быть не protected.
Введите описание `practice-docker-runner`. Нажмите Create runner.
GitLab покажет фактический **runner authentication token**, обычно с префиксом `glrt-`. Это не устаревший registration token.

**Здесь остановитесь и получите реальный токен из интерфейса. Не выполняйте регистрацию с вымышленным значением.** Токен не нужно отправлять в чат. Вставьте его локально в запрос скрытого ввода:

```bash
read -rsp 'Runner authentication token: ' RUNNER_AUTH_TOKEN
printf '\n'
docker compose exec runner gitlab-runner register \
  --non-interactive \
  --url 'http://gitlab.local:8080' \
  --token "$RUNNER_AUTH_TOKEN" \
  --executor docker \
  --docker-image 'python:3.12-slim' \
  --docker-network-mode 'gitlab-practice-net' \
  --description 'practice-docker-runner'
unset RUNNER_AUTH_TOKEN
docker compose restart runner
docker compose exec runner gitlab-runner verify
docker compose logs --tail=100 runner
```

Executor Docker создаёт отдельный контейнер для каждого job. Runner получает доступ к Docker хоста через `/var/run/docker.sock`. Этот учебный Runner используйте только для доверенных проектов своей группы; job-контейнерам socket не передаётся, privileged не нужен.
Volume runner-config сохраняет регистрацию. Docker-сеть gitlab-practice-net даёт Runner и job-контейнерам доступ к gitlab.local:8080, включая checkout и artifacts. Одного hosts-файла на компьютере для контейнеров недостаточно — поэтому сеть задана явно.

Откройте Admin → CI/CD → Runners, обновите страницу и дождитесь **Online**. `verify` проверяет регистрацию, но сам по себе не доказывает Online или выполнение jobs.

## Шаг 6. Создать четыре отдельных проекта

Для каждого проекта: верхний `+` / New project → Create blank project.
Namespace: созданная группа practice-2. Visibility: Private. Снимите **Initialize repository with a README**, чтобы репозиторий был пустым.

| Студент | Project name / slug | Локальная папка |
|---|---|---|
| 1 | student-1-todo-api | project-1-todo-api |
| 2 | student-2-student-planner | project-2-student-planner |
| 3 | student-3-text-analyzer | project-3-text-analyzer |
| 4 | student-4-sales-report | project-4-sales-report |

В каждом проекте Settings → CI/CD → Runners проверьте, что instance runners включены и общий Runner доступен. Если есть кнопка Enable instance runners — включите.

## Шаг 7. Настроить доступ Git

Для локальной учебной среды используйте HTTP Clone URL. При push нужен Personal Access Token вместо пароля, если парольная аутентификация Git отключена.
Под своей учётной записью: аватар → Edit profile → Access tokens → Add new token. Название `practice-git`, срок действия на время работы, scope **write_repository**. Создайте и сохраните фактический токен локально. В терминале при push username — ваш GitLab username, password — этот токен. Не помещайте токен в remote URL или файлы проекта.

Откройте соответствующий проект → Code / Clone → **Clone with HTTP** → скопируйте фактический URL. Это URL репозитория, а не адрес страницы Pipelines.
В следующих блоках `read` предлагает вставить именно скопированный URL, без придуманных адресов.
Если Git ещё не настроен, из корня комплекта:

```bash
read -rp 'Ваше имя для Git commits: ' COMMIT_NAME
read -rp 'Ваш email для Git commits: ' COMMIT_EMAIL
git config --global user.name "$COMMIT_NAME"
git config --global user.email "$COMMIT_EMAIL"
```

## Шаг 8. Загрузить каждый проект

Выполняйте из корня распакованного gitlab-practice. Каждый блок создаёт отдельный репозиторий. Эти команды — для первого запуска, не повторяйте `remote add` в уже настроенном репозитории.

### Студент 1

```bash
cd project-1-todo-api
git init
git add .
git commit -m "Initial Todo API with CI"
git branch -M main
read -rp 'Вставьте HTTP Clone URL student-1-todo-api: ' REPO_URL
git remote add origin "$REPO_URL"
git push -u origin main
cd ..
```

### Студент 2

```bash
cd project-2-student-planner
git init
git add .
git commit -m "Initial Student Planner with CI"
git branch -M main
read -rp 'Вставьте HTTP Clone URL student-2-student-planner: ' REPO_URL
git remote add origin "$REPO_URL"
git push -u origin main
cd ..
```

### Студент 3

```bash
cd project-3-text-analyzer
git init
git add .
git commit -m "Initial Text Analyzer with CI"
git branch -M main
read -rp 'Вставьте HTTP Clone URL student-3-text-analyzer: ' REPO_URL
git remote add origin "$REPO_URL"
git push -u origin main
cd ..
```

### Студент 4

```bash
cd project-4-sales-report
git init
git add .
git commit -m "Initial Sales Report with CI"
git branch -M main
read -rp 'Вставьте HTTP Clone URL student-4-sales-report: ' REPO_URL
git remote add origin "$REPO_URL"
git push -u origin main
cd ..
```

## Шаг 9. Проверить фактические pipeline

После push в каждом проекте:

1. Откройте Build → Pipelines (в старых версиях CI/CD → Pipelines).
2. Откройте pipeline последнего commit на main.
3. Дождитесь последовательного завершения build → test → deploy.
4. Нажмите build_job, прочитайте лог: должна реально выполниться `python tools.py build`.
5. Откройте test_job: должны быть результаты unittest и Application smoke: PASS.
6. Откройте deploy_job: должен быть Educational deploy: PASS.
7. В deploy_job откройте Job artifacts → Browse / Download. Проверьте app.py и manifest.json внутри deploy/.
8. Повторите для всех четырёх проектов.

Ожидаемый, **пока не подтверждённый** результат: build PASSED, test PASSED, deploy PASSED.
Jobs выполняются автоматически; manual и needs не используются. Порядок задаёт stages, ZIP передаётся через artifacts и dependencies.
Если нужен повторный запуск без commit: Build → Pipelines → New pipeline / Run pipeline → main → Run pipeline.

## Шаг 10. Если job упал или остался Pending

Откройте конкретный job и скопируйте настоящий лог от команды до ошибки (без секретов). Для Pending откройте сообщение о подходящих Runner и проверьте Online, Run untagged jobs, Protected и доступность instance runner в проекте.
Не отмечайте pipeline успешным до фактического зелёного результата.
Пришлите в чат лог, имя проекта и job; исправление должно опираться на эту ошибку.
После конкретного исправления в папке соответствующего проекта:

```bash
python -m unittest discover -s tests -v
python tools.py build
python tools.py smoke dist/application.zip
python tools.py deploy
git add .
git commit -m "Fix CI failure"
git push
```

Откройте новый pipeline и проверьте все три stages. При сообщении о некорректном YAML используйте Build → Pipeline editor → Validate / CI Lint в установленном GitLab. Встроенная проверка YAML в GitLab ещё не выполнялась в этом комплекте.

## Шаг 11. Скриншоты после успеха

Общие для группы: главная страница локального GitLab с адресом; Runner со статусом Online.
Для каждого студента:

1. Страница своего Project и список файлов Repository (можно объединить).
2. Свой app.py — содержательная часть логики.
3. Свой .gitlab-ci.yml целиком с тремя stages.
4. Pipeline с тремя зелёными jobs и указанием commit/ветки.
5. Лог успешного build_job с настоящей командой.
6. Лог успешного test_job с количеством тестов и smoke.
7. Лог успешного deploy_job и artifacts/deploy (если помещаются — объединить).

Лучше всего требования доказывают **Runner Online, YAML, общий зелёный pipeline и реальные логи трёх jobs**. Не фотографируйте authentication token, PAT или пароль.
Это список для будущих фактических снимков; скриншоты успеха здесь не сгенерированы.

## Шаг 12. Рассказ на 1–2 минуты

Следующий текст используйте после фактической проверки GitLab:

«Мы развернули локальный GitLab в Docker. Это сервер, где находятся наши репозитории и запускаются pipeline. У каждого из четырёх студентов отдельный проект с собственной программой, тестами и CI-конфигурацией.

Runner — отдельная программа, которая подключается к GitLab, получает задания и выполняет их. Мы выбрали Docker executor: каждый job запускается в отдельном контейнере Python.

Файл .gitlab-ci.yml описывает pipeline. Pipeline — весь процесс проверки и подготовки программы. Stage — этап, а job — конкретное задание с командами. У нас три этапа: build, test и deploy.

На build Python проверяет компиляцию исходника, затем собирается ZIP-пакет. GitLab сохраняет его как artifact и передаёт следующим заданиям. На test запускаются настоящие автоматические тесты логики и проверяется приложение из собранного ZIP. Для моего проекта это [назовите свою функцию и проверку]. Ошибка в проверяемой логике приводит к падению теста.

На deploy ZIP распаковывается в папку deploy, проверяется запуск и создаётся файл контрольных сумм. Это учебный deploy, не постоянный production-сервис. После push GitLab автоматически создал pipeline, Runner выполнил задания по порядку, и мы проверили их статус и логи».

## Остановка и повторный запуск

Из infrastructure:

```bash
docker compose stop
# Следующий запуск с сохранением данных:
docker compose up -d
```

Именованные volumes сохраняют пользователей, проекты и регистрацию Runner. `docker compose down` удаляет контейнеры и сеть, но сохраняет volumes. Не используйте `down -v`: это удаляет данные работы.
