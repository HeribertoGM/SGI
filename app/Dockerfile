FROM python:3.8.2

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD waitress-serve --host $APP_HOST --port $APP_PORT --call config:create_app