# Проверки комплекта

Повторно выполнены команды приложений в Python 3.12.14 в среде подготовки GitHub-комплекта. Это не новый запуск GitLab pipeline.

- project-1-todo-api: tests/build/smoke/deploy PASS
- project-2-student-planner: tests/build/smoke/deploy PASS
- project-3-text-analyzer: tests/build/smoke/deploy PASS
- project-4-sales-report: tests/build/smoke/deploy PASS
- sales-report-deploy_job-27-artifacts.zip: manifest SHA256 PASS
- todo-api-deploy_job-18-artifacts.zip: manifest SHA256 PASS
- text-analyzer-deploy_job-24-artifacts.zip: manifest SHA256 PASS
- student-planner-deploy_job-21-artifacts.zip: manifest SHA256 PASS

В сохранённых логах всех 12 jobs есть Job succeeded. Pipeline: Todo #6, Planner #7, Analyzer #8, Sales #9. Текущий Online локального Runner здесь повторно не проверялся.

Проверены типовые форматы токенов и приватных ключей в текстовых файлах.
