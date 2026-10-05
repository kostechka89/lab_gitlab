# Повторный запуск на Windows

Среда уже установлена: группа devopsrabota2, Runner devops-docker. Данные хранятся в Docker volumes.

## PowerShell

Запустить Docker Desktop через меню Пуск и дождаться успешного `docker info`.

```powershell
Set-Location 'C:\Users\kokstik\lab_gitlab-main\gitlab-practice\infrastructure'
docker compose up -d --pull never gitlab runner
docker compose ps
curl.exe --noproxy '*' -I http://gitlab.local:8080
docker compose exec runner gitlab-runner verify
```

GitLab запускается несколько минут. HTTP 302 на страницу входа — нормальный ответ.
Остановить без потери данных: `docker compose stop`. Возобновить командами выше.

Открыть отдельный Chrome:

```powershell
Start-Process -FilePath 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList @("--user-data-dir=$env:LOCALAPPDATA\GitLabChrome",'--no-proxy-server','--disable-extensions','http://gitlab.local:8080/devopsrabota2')
```

## CMD

```cmd
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
cd /d C:\Users\kokstik\lab_gitlab-main\gitlab-practice\infrastructure
docker compose up -d --pull never gitlab runner
docker compose ps
curl.exe --noproxy "*" -I http://gitlab.local:8080
docker compose exec runner gitlab-runner verify
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="%LOCALAPPDATA%\GitLabChrome" --no-proxy-server --disable-extensions "http://gitlab.local:8080/devopsrabota2"
```

Остановить: `docker compose stop` в той же папке. Пароль вводить только на странице GitLab.

## После перезагрузки

Запустить Docker Desktop, дождаться Engine, повторить команды запуска.
В hosts уже есть `127.0.0.1 gitlab.local`.
Для диагностики использовать `docker compose ps` и `docker compose logs --tail 80 gitlab`.
Сайт: порт 8080; Puma: внутренний 8081; SSH: 2222. Сеть Runner/jobs: gitlab-practice-net.
Если curl работает, а обычный браузер выдаёт 503, открыть отдельный профиль командой выше.
Не удалять volumes и не выполнять сброс или переустановку среды для обычного восстановления.

## Проекты, pipeline и участники

Открыть http://gitlab.local:8080/devopsrabota2 и выбрать проект.
В Build → Pipelines открыть pipeline и jobs build_job, test_job, deploy_job.
У deploy_job скачать artifacts. Стандартный срок YAML — одна неделя; новые проверенные artifacts сохранены через Keep и скопированы в submission/evidence.

Позднее root может создать реальные учётные записи через Admin → Users → New user.
В нужном проекте Manage → Members → Invite members выбрать пользователя и роль Developer.
Каждому дать доступ к его проекту. Не придумывать персональные данные и не сохранять пароли в документах.
Для последующего push по HTTP: `git -c http.proxy= push origin main`, авторизация интерактивная.
Для последующей работы используется личная авторизация участника.
