FROM python:3.9.6-slim-buster

ENV PYTHONUNBUFFERED=1
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt 

WORKDIR /home/project
COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "base.wsgi"] 