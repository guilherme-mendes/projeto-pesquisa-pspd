FROM openjdk:8-slim
COPY --from=python:3.8 . .

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . ./

ENTRYPOINT [ "python3", "-u", "./word_count.py" ]
