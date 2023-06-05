FROM python:slim-buster

COPY . /code
WORKDIR /code

RUN apt-get update
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "-m", "src.cli"]
