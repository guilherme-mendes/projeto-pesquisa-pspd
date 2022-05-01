FROM python:3.8

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade setuptools wheel
RUN pip3 install -r requirements.txt

RUN mkdir /src

COPY ./src/ /src/

WORKDIR /src
