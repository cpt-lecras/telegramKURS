FROM python:3.12-slim-bullseye

COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

RUN chmod 777 ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]