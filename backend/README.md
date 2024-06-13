# Backend для сайта Foodgram
***
> __Используемые технологии__
>> ___Django___ -  фреймворк для веб-приложений на языке Python.
>> ___Django REST Framework___ - обеспечивает взаимодействие клиента с сайтом на сервере через API.
>> ___Djoser___ -  пакет реализующий аутентификацию по токенам.
>> ___Gunicorn___ -  WSGI Pytnon-сервер.
>> ___PostgreSQL___ - объектно-реляционная система управления базами данных. (Используется при развертывании проэкта через docker compose)
***
> __Список используемых библиотек__
``` python
Django==3.2.3
djangorestframework==3.12.4
django-cors-headers==3.13.0
django-filter==23.1
django-link-shortener==0.5
djoser==2.1.0

gunicorn==20.1.0 

flake8==6.0.0
flake8-isort==6.0.0

psycopg2-binary==2.9.3
Pillow==9.0.0
```
***
> ___Примеры API___[^1]
>> `GET api/users/`
```python
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/?page=4",
  "previous": "http://foodgram.example.org/api/users/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Иванов",
      "is_subscribed": false,
      "avatar": "http://foodgram.example.org/media/users/image.png"
    }
  ]
}
``` 
>> `POST api/users/`
```python
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Иванов",
  "password": "Qwerty123"
}
```
>> `GET api/recipes/`
```python
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Иванов",
        "is_subscribed": false,
        "avatar": "http://foodgram.example.org/media/users/image.png"
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.png",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```
>> `POST api/recipes/`
```python
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
***
В файле config директории base установите значение DEVELOP в True, если вы в начале разработке, или False, если готовитесь развернуть проэкт на сервере.
[^1]: OpenApi doc доступна после выполнения docker compose up в папке infra, по адресу http://localhost/api/docs/