FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=true
ENV PYTHONDONTWRITEBYTECODE=true

WORKDIR /app

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get -y install netcat

COPY ./entrypoint.sh .

COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]