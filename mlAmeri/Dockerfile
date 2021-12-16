FROM python:3.8.3-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

COPY . .

ARG name

RUN apk update \
    && apk update \
    && apk add --virtual build-deps \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && pip install numpy \
    && pip install matplotlib \
    && pip install tensorflow \
    && pip install opencv-python \
    && apk del build-deps

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
