# Практическая работа №2: GitLab CI/CD

Готовый комплект из четырёх разных индивидуальных проектов.

**Начните с [пошаговой инструкции](gitlab-practice/GUIDE.md).**

| Проект | Назначение |
|---|---|
| [Todo REST API](gitlab-practice/project-1-todo-api/) | HTTP API задач |
| [Student Planner](gitlab-practice/project-2-student-planner/) | Веб-планировщик учебных заданий |
| [Text Analyzer CLI](gitlab-practice/project-3-text-analyzer/) | Консольный анализ текста |
| [CSV Sales Report](gitlab-practice/project-4-sales-report/) | Пакетное создание HTML-отчёта из CSV |

В каждой папке: исходный код, README, зависимости, тесты, сборка, учебный deploy и собственный `.gitlab-ci.yml` с этапами build → test → deploy.

- [Docker Compose для GitLab и Runner](gitlab-practice/infrastructure/compose.yaml)
- [Фактические локальные проверки](gitlab-practice/LOCAL-VERIFICATION.txt)

Локально прошли 15 автоматических тестов, запуск приложений, сборка и учебный deploy. Проверено, что намеренные ошибки логики вызывают падение тестов.
GitLab pipeline и Runner Online пока не подтверждены: выполните инструкцию на своём компьютере.

Этот GitHub-репозиторий хранит комплект для скачивания. Для сдачи работы создайте **четыре отдельных GitLab-репозитория** и загрузите в каждый только содержимое соответствующей папки project-*. Не загружайте весь комплект в один студенческий репозиторий.

Для скачивания в GitHub нажмите **Code → Download ZIP**, распакуйте архив и откройте `gitlab-practice/GUIDE.md`.
