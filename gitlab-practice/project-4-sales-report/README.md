# CSV Sales Report

Индивидуальный независимый репозиторий для практической работы №2.
Требуется Python 3.12. Внешних библиотек нет; requirements.txt явно фиксирует это.

## Установка и запуск

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --no-index -r requirements.txt
python app.py sample.csv --output report.html
```

Windows PowerShell: `.venv\Scripts\Activate.ps1` вместо `source`.

Входные файлы — UTF-8. Некорректный вход возвращает код 2.

## Проверки и CI

```bash
python -m unittest discover -s tests -v
python tools.py build
python tools.py smoke dist/application.zip
python tools.py deploy
```

Build компилирует код и упаковывает исходники, примеры и README в ZIP.
Test проверяет логику и запускает приложение из распакованного build artifact.
Deploy распаковывает этот artifact в deploy/, повторно проверяет запуск и создаёт SHA256-манифест.
Это учебный deployment artifact, а не публикация постоянно работающего сервиса.
В GitLab каждый job работает в отдельном контейнере; ZIP передаётся через artifacts.
Запуск развёрнутой программы: `cd deploy`, затем команда запуска выше.

Для GitLab используйте общий GUIDE.md из комплекта; загрузите только содержимое этой папки в свой репозиторий.
