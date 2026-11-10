# Лабораторная работа №10: Настройка CI/CD с использованием GitHub Actions

## 1. Структура проекта
- `index.html` — веб-страница формы создания персонажа D&D 5e;
- `test_ui.py` — 4 автоматизированных UI-теста на Selenium (headless Chrome);
- `.github/workflows/ci.yml` — конфигурационный пайплайн GitHub Actions.

## 2. Схема ветвления (Git Flow)
1. `main` — стабильная production-ветка, из которой происходит автоматический деплой на GitHub Pages после прохождения тестов.
2. `dev` — основная интеграционная ветка разработки.
3. `fix/character-validation` — рабочая ветка для исправления ошибок или добавления фич, отводимая от `dev`.

## 3. Пошаговый сценарий работы с ветками и Pull Request
```bash
git checkout dev
git checkout -b fix/character-validation

git add .
git commit -m "Fix validation message in character form"
git push origin fix/character-validation
```

- На GitHub создается Pull Request: `fix/character-validation` -> `dev`.
- GitHub Actions автоматически запускает job `test`.
- При успешном прохождении тестов выполняется merge PR в ветку `dev`.
- Создается второй Pull Request: `dev` -> `main`.
- После завершения финальной проверки тестов выполняется merge в `main`.
- Триггерится job `deploy`, который публикует приложение на GitHub Pages.
