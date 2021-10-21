# base image
FROM python:3.9

LABEL Author="Joe"

ENV PYTHONBUFFERED 1

RUN mkdir /src
WORKDIR /src
COPY src/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY /src /src

