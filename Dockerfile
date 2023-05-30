FROM python:slim-buster

COPY . /code
WORKDIR /code

RUN apt-get update
RUN pip install -r requirements.txt

ENV LIBRARY_CATALOUGE_SERVER="https://catalogue.library.cern"
ENV LIBRARY_CATALOUGE_SERVER_SUFFIX="/api/literature/?q="

ENTRYPOINT ["python3", "-m", "src.cli"]
