FROM python:3.8

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install -y locales locales-all

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/adlt-sa.json
ENV GCP_PROJECT=GCP_PROJECT

ENV LC_ALL="es_ES.UTF-8"
ENV LC_CTYPE="es_ES.UTF-8"

COPY . /app

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]