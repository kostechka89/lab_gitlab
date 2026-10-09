# Практическая работа №2 — GitLab CI/CD

Четыре индивидуальных приложения на общей локальной установке GitLab и Runner.

## Материалы команды

| Участник | Проект | Что открыть |
|---|---|---|
| Костя | Todo REST API и общая инфраструктура | [Материал Кости](team/01-KOSTYA.md) |
| Дима | Student Planner | [Материал Димы](team/02-DIMA.md) |
| Лариса | CSV Sales Report | [Материал Ларисы](team/03-LARISA.md) |
| Настя | Text Analyzer CLI | [Материал Насти](team/04-NASTYA.md) |

Начните с [общего текста выступления](team/TEAM-SPEECH.md) и [сценария показа на ПК Кости](team/PC-DEMO.md). Подробности своего приложения — в материалах участников; краткий [порядок защиты](team/DEFENSE-ORDER.md) сохранён отдельно.

## Отчёт и запуск

- [Word-отчёт с местами для скриншотов](reports/Отчёт-ПР2-GitLab-CICD.docx)
- [Что проверить и заполнить в отчёте](reports/REPORT-REVIEW.md)
- [Повторный запуск на Windows](WINDOWS-RUNBOOK.md)
- [Проверка сохранённых доказательств](CHECKS.md)
- [Архив для скачивания](downloads/gitlab-practice-submission.zip)

## Исходники

- [Todo API](gitlab-practice/project-1-todo-api/)
- [Student Planner](gitlab-practice/project-2-student-planner/)
- [Sales Report](gitlab-practice/project-4-sales-report/)
- [Text Analyzer](gitlab-practice/project-3-text-analyzer/)
- [Docker Compose](gitlab-practice/infrastructure/compose.yaml)

В GitLab приложения находятся в четырёх отдельных репозиториях группы devopsrabota2. Этот GitHub хранит общий комплект для скачивания и защиты, а не заменяет индивидуальные GitLab-проекты.

Сохранённые логи подтверждают pipeline #6, #7, #8 и #9. Адрес gitlab.local работает на компьютере с установленным сервером и не открывается у других автоматически. Deploy — подготовка проверенного пакета файлов, без постоянного production-сервиса.

Костя настраивал общую среду и загружал проекты. Индивидуальные проекты распределены между участниками; описание личного вклада каждый заполняет по фактически выполненным действиям.
