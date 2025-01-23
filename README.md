# API для сервиса SelfStorage

## Описание моделей
- `Consent` - модель согласия для обработки персональных данных

- `Contract` - модель заказа, связана с:
  
    - `PickupLocation` - место хранения и самовывоза
    - `StorageRate` - модель тарифов

## Установка

Python3 должен быть уже установлен. 

- Клонируйте репозиторий:

```
git clone https://github.com/Eugene571/beauty_city_bot.git
```

- Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

- Создайте БД командой:
  
```
python3 manage.py migrate
```

- Запуск:

```
python3 manage.py runserver
```

## API
