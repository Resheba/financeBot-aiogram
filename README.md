# short 
Telegram бот, позволяющий заполнять Google Sheet таблицу соответствуюими данными. Встроен функционал парсинга данных из имеющихся листов с последующей интеграцией этих данных в работу бота. 
# Быстрый старт в 3 шага
### Первый шаг. Получить токены
Нам понадобятся токены:
- **Telegram** токен для бота;
    >Получить его можно через [BotFather](https://t.me/BotFather "BotFather")
- **Google** токены для доступа к таблицам;
    + Понадобится *Client Secret Credentials*, он имеет следующий формат: 
        ```JSON 
        {
        "installed": {
            "client_id": "12345678901234567890abcdefghijklmn.apps.googleusercontent.com",
            "project_id": "my-project1234",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "...": "..."
            }
        }
        ```
    + Ещё нужен авторизированный пользователь, он имеет следующий формат:
        ```JSON
        {
            "refresh_token": "8//ThisALONGTOkEn....",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": "12345678901234567890abcdefghijklmn.apps.googleusercontent.com",
            "client_secret": "MySecRet....",
            "scopes": [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ],
            "expiry": "1070-01-01T00:00:00.000001Z"
        }
        ```
        >Подробнее вся информация [здесь](https://docs.gspread.org/en/v5.10.0/oauth2.html#enable-api-access-for-a-project "Документация").
### Второй шаг. Заполнить файл окружения
Создаём файл `.env` в корне директории и заполняем его соответствующими данными, полученнми ранее.
````bash
CREDENTIALS={"installed":{"client_id":"8OcsRJawdADar3cAM1qEGTJP"...."redirect_uris":["http://localhost"]}}
AUTH_USER={"refresh_token": "1GomaKZ1АСP1Dro7wA", "token_uri": ... "expiry": "2000-01-01T01:01:01.00001Z"}

TELEGRAM_TOKEN=....

TABLE_NAME=Finance

LIST_USER_NAME=Users
LIST_OPERATIONS_NAME=Operations
LIST_DIRECTIOINS_NAME=_directions
LIST_OPERATIONS_TYPES_NAME=_operations_types
````
Сохраняем и переходим к завершающему пункту.
### Третий шаг. Установить зависимости и запустить
Осталось лишь написать 2 команды в консоль:
+ Установка зависимостей:
    ````BASH
    pip install -r requirements.txt
    ````
+ Запуск приложения:
    ````BASH
    python3 main.py
    ````
    >Команды для запуска могут отличаться на разных ОС (Windows: `python main.py`)
### Замечания
+ В `.env` файле необходимо также указать названия листов с соответствующими данными.
+ `CREDENTIALS` в файле `.env` должены быть введены в одну строку. Без переносов.
+ `AUTH_USER` в файле `.env` также заполняется в одну строкй, как и `CREDENTIALS`.
