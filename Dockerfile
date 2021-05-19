FROM python:3.9.5

ENV FLASK_APP=app/index \
    FLASK_ENV=development

WORKDIR /maru65536_family

COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install libmariadb-dev && \
    pip3 install -r requirements.txt

CMD ["flask", "run"]