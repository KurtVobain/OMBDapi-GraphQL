FROM python:3.10.4-slim-buster

WORKDIR /usr/src/app

COPY app app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY .env boot.sh ./
RUN chmod +x boot.sh


ENTRYPOINT ["./boot.sh"]