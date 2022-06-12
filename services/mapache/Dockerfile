FROM python:3.8

RUN pip install scrapyrt

RUN apt-get update
RUN apt-get install -y locales locales-all

ENV LC_ALL="es_ES.UTF-8"
ENV LC_CTYPE="es_ES.UTF-8"

COPY . /app

WORKDIR /app

CMD ["scrapyrt", "-i", "0.0.0.0"]