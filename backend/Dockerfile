FROM python:3.9.6-slim-buster

ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install wkhtmltopdf -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 

WORKDIR /home/project
COPY . .

EXPOSE 8000
