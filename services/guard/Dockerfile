FROM composer:2.3.5 as vendor

WORKDIR /tmp/

COPY composer.json composer.json

RUN composer install \
    --ignore-platform-reqs \
    --no-interaction \
    --no-plugins \
    --no-scripts \
    --prefer-dist


FROM php:8.1-apache-buster

RUN apt-get update && apt-get install -y libpq-dev

RUN docker-php-ext-configure pgsql -with-pgsql=/usr/local/pgsql
RUN docker-php-ext-install pdo pdo_pgsql pgsql

COPY . /var/www/html
COPY --from=vendor /tmp/vendor/ /var/www/html/vendor/