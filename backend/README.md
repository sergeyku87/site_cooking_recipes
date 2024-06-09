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