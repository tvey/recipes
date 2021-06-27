FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --skip-lock --system --dev
RUN apt-get update \
    && apt-get -y install netcat
COPY ./entrypoint.sh .
COPY . ./
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]