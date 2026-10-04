# Участник 2: Student Planner

## 1. Что вам нужно и что вводить

Внешние API и Telegram не нужны. Задания вводятся через форму в браузере.
Данные хранятся в памяти и исчезают после перезапуска. База данных для этой работы не требуется.

Ваш проект: `student-2-student-planner`. Только вы загружаете содержимое `project-2-student-planner` в этот репозиторий.
Не загружайте четыре приложения в один студенческий репозиторий.

Перед началом один участник группы должен развернуть общий GitLab и зарегистрировать Runner по [общей инструкции](../GUIDE.md), шаги 1–6.
GitLab и Runner общие; отдельный GitLab или отдельный Runner каждому студенту не требуется.
Runner authentication token вводит только ответственный за общую среду при регистрации. В файлы приложения или `.gitlab-ci.yml` его не вставляют.

В общей инструкции выбран адрес http://gitlab.local:8080. Он работает на компьютере с установленным GitLab и записью hosts.
Самый простой вариант для группы — выполнять загрузку и проверку всех четырёх проектов на этом компьютере, входя под соответствующим пользователем GitLab.
Если работаете с разных компьютеров, localhost у каждого свой: сначала нужен доступ к компьютеру с GitLab и правильный адрес/hosts. Не подставляйте чужой localhost; согласуйте сеть с ответственным за среду.

## 2. Получить файлы и установить Python

Откройте GitHub-репозиторий [lab_gitlab](https://github.com/kostechka89/lab_gitlab) → Code → Download ZIP, распакуйте.
Откройте терминал **внутри** `gitlab-practice/project-2-student-planner`.
Команды рассчитаны на Bash, Linux/macOS или WSL2. Требуется Python 3.12; на Linux/macOS системная команда может называться python3.

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --no-index -r requirements.txt
```

Если Python не установлен, установите Python 3.12 до этих команд. В Ubuntu для venv может понадобиться пакет python3-venv.
Зависимости — только стандартная библиотека; requirements.txt не требует скачивания сторонних пакетов.
Windows PowerShell: `python -m venv .venv`, затем `.venv\Scripts\Activate.ps1`; остальные примеры с read/printf выполняйте в Bash/WSL.

## 3. Запустить своё приложение

```bash
python app.py --port 8002
```

Откройте http://localhost:8002/.

1. В Subject введите `DevOps`, в Assignment — `Practical work 2`.
2. Нажмите Add assignment. Проверьте, что появилось задание со статусом Pending.
3. Нажмите complete у задания. Статус должен стать Completed.
4. Нажмите delete. Задание должно исчезнуть.
5. Добавьте ещё одно своё учебное задание для демонстрации.

Это данные приложения; они не требуют редактирования токенов или CI-конфигурации.

Остановите сервер Ctrl+C перед следующими проверками или используйте второй терминал с активированным venv.

## 4. Проверить тесты, сборку и deploy

В папке приложения, с активированным venv:

```bash
python -m unittest discover -s tests -v
python tools.py build
python tools.py smoke dist/application.zip
python tools.py deploy
```

Тесты проверяют: добавление, завершение, удаление, обязательные поля и безопасное отображение HTML.
Smoke отправляет формы по HTTP и проверяет появление, завершение и удаление задания.
Build создаёт dist/application.zip после проверки компиляции; deploy распаковывает ZIP в deploy/, проверяет запуск и создаёт manifest.json с SHA256.
Это учебный deployment artifact. Постоянный сервис автоматически не публикуется.
До GitLab эти команды реально проверены автором комплекта; свой запуск и pipeline подтвердите самостоятельно.

## 5. Создать свой GitLab Project

1. Откройте общий GitLab в браузере и войдите под своей учётной записью.
2. Если проект `student-2-student-planner` уже создан ответственным, откройте его и пропустите создание.
3. Иначе нажмите New project → Create blank project.
4. Project name / slug: `student-2-student-planner`. Namespace: группа `practice-2` из общей инструкции.
5. Visibility: Private. Снимите Initialize repository with a README.
6. Нажмите Create project.
7. Settings → CI/CD → Runners: убедитесь, что общий instance runner доступен и Online. При необходимости включите Enable instance runners.
8. Для этих YAML у Runner должен быть включён Run untagged jobs; Protected не должен мешать запуску на main.

## 6. Подготовить доступ и скопировать настоящий URL

1. В своём проекте нажмите Code / Clone → Clone with HTTP.
2. Скопируйте показанный **фактический URL** именно `student-2-student-planner`.
3. Для push создайте свой Personal Access Token: аватар → Edit profile → Access tokens → Add new token; scope write_repository, срок действия на время работы.
4. Сохраните фактический токен локально. При git push username — ваш GitLab username, password — этот PAT, если сервер требует токен вместо пароля.

PAT для Git и authentication token Runner — разные токены. Telegram-токена здесь нет.
Не вставляйте PAT в код, YAML или remote URL. Не отправляйте токены в чат и не показывайте на скриншотах.

## 7. Загрузить только свой проект

Выполните в папке `project-2-student-planner`, а не в корне скачанного комплекта.
Если скачали ZIP, в этой папке ещё нет собственного Git-репозитория.
Если вместо ZIP клонировали общий GitHub-репозиторий, сначала скопируйте свою папку **за пределы клона** и выполняйте команды в этой копии, чтобы не использовать родительский .git.

```bash
git init
read -rp 'Ваше имя для commit: ' COMMIT_NAME
read -rp 'Ваш email для commit: ' COMMIT_EMAIL
git config user.name "$COMMIT_NAME"
git config user.email "$COMMIT_EMAIL"
git add .
git commit -m "Initial Student Planner with CI"
git branch -M main
read -rp 'Вставьте HTTP Clone URL вашего проекта student-2-student-planner: ' REPO_URL
git remote add origin "$REPO_URL"
git push -u origin main
```

Перед push можно проверить `git remote -v`: URL должен вести к вашему проекту.
Эти команды для первой загрузки; не повторяйте remote add, если origin уже настроен.

## 8. Проверить свой pipeline

1. В **своём** Project откройте Build → Pipelines.
2. Откройте pipeline нового commit на main.
3. Дождитесь build_job → test_job → deploy_job.
4. Откройте каждый job и прочитайте лог.
5. Build: реальная команда упаковки и Build: PASS.
6. Test: реальные результаты unittest и Application smoke: PASS.
7. Deploy: Educational deploy: PASS. Job artifacts → Browse покажет deploy/app.py и deploy/manifest.json.

Ожидаемый результат — три Passed. Сейчас успех вашего GitLab pipeline ещё не подтверждён.
Если Pending, проверьте доступность Runner и его настройки. Если Failed, скопируйте **настоящий лог** упавшего job, имя проекта и commit и пришлите для разбора. Не вставляйте секреты.
После исправления выполните локальные проверки из шага 4, затем:

```bash
git add .
git commit -m "Fix CI failure"
git push
```

Проверьте новый pipeline. Не делайте исправления наугад без сообщения об ошибке.

## 9. Что показать преподавателю

Сохраните снимки своего Project/Repository, app.py, .gitlab-ci.yml, зелёного pipeline и логов build/test/deploy. Общий снимок Runner Online можно использовать всей группой.
Добавьте снимок работы своего приложения из шага 3. Не подменяйте реальный успешный pipeline локальным логом.

Для защиты объясните:

«Мой проект — Student Planner. Тесты проверяют добавление, завершение, удаление, обязательные поля и безопасное отображение HTML. После push GitLab читает мой .gitlab-ci.yml и создаёт pipeline. Общий Runner выполняет jobs в отдельных Docker-контейнерах. Build собирает ZIP; test проверяет логику и запуск собранного приложения; deploy готовит проверенный пакет и контрольные суммы. У меня отдельный репозиторий и отдельный pipeline».

Про фактический успех говорите после прохождения всех трёх jobs.
