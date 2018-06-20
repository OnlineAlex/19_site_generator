# Энциклопедия

Генератор статей в формате Markdown на сайт.

[Пример сайта](https://onlinealex.github.io/19_site_generator/)

# Как работать

### Требования
Скрипт требует для своей работы установленного интерпретатора
Python версии 3.5 выше

И  пакетов из requirements.txt
```bash
pip install -r requirements.txt # или командой pip3
```

Помните, рекомендуется использовать
[virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/)
для лучшего управления пакетами.

По умолчанию `build.py` генерирует html статьи в формате .md
из папки `/articles`. И добавляет их на главную старницу.

## Как запускать

Стандатной командой `python` (на некоторых компьютерах `python3`)

```bash
$ python build.py
```
> Запуск для всех ОС одинаковый

# Цели проекта
Код создан в учебных целях. В рамках учебного курса по
веб-разработке - [DEVMAN.org](https://devman.org)