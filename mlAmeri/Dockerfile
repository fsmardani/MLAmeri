#FROM python:3.9-alpine
#
#WORKDIR .
#
#ENV PYTHONDONTWRITEBYTECODE 1
#
#COPY . .
#
#ARG name
#
#RUN apk update \
#    && apk add --virtual build-deps \
#    && apk add --virtual build-deps gcc python3-dev musl-dev \
#    && apk add jpeg-dev zlib-dev libjpeg \
#    && pip install Pillow \
#    && apk del build-deps
#
#RUN pip install --upgrade pip
#
#RUN pip install -r requirements.txt

FROM python:3.8-buster
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
COPY . .
ARG name
RUN mkdir temp && mkdir Output && mkdir Input && mkdir media


RUN apt-get update
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt




