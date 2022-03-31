FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

RUN apt-get update
RUN apt-get install -y python3-psycopg2 python3-dev libpq-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /app/
COPY ./entrypoint.sh /entrypoint.sh
COPY .env /app/.env

RUN chmod +x /entrypoint.sh
RUN chown -R $UID:$GID /app
RUN chown $UID:$GID entrypoint.sh
RUN chmod -R 775 /app


CMD [ "/entrypoint.sh" ]
