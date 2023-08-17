FROM python:3.11-alpine
LABEL authors="dzigr"

ENV PYTHONUNBUFFERED 1

WORKDIR /project

ADD requirements.txt /project/

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev \
                        bash \
                        postgresql-dev \
                        gettext

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade pip setuptools wheel

RUN pip3 install -r requirements.txt

ADD . /project
