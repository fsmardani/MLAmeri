FROM python:3.9-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

COPY . .

ARG name

RUN apk update \
    && apk add --virtual build-deps \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

RUN pip install --upgrade pip

RUN sudo pip install -r requirements.txt
