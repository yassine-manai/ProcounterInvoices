FROM python:3.12-slim


WORKDIR /app
COPY . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# tzdata for timzone
RUN apt-get update -y
RUN apt-get install -y tzdata
 
# timezone env with default
ENV TZ=UTC

ENV APP_IP=127.0.0.1
ENV ZR_PORT=8200

ENV ZR_IP=192.168.1.7
ENV SERVER_PORT=8000


ENV PROCOUNTOR_URL=https://pts-procountor.pubdev.azure.procountor.com/api
ENV PROCOUNTOR_URL_TOKEN=https://pts-procountor.pubdev.azure.procountor.com/api/oauth/token
ENV GRANT_TYPE=client_credentials
ENV CLIENT_ID=ParktechTestClient
ENV CLIENT_SECRET=secret_RKoUMBMKLMsGYqYiri9h1ubNVKUDBqLSutxxVmYwqxD4eYfrGi
ENV API_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIyODI2NCIsImF1ZCI6IlBhcmt0ZWNoVGVzdENsaWVudCIsImlzcyI6Imh0dHBzOi8vcHRzLXByb2NvdW50b3IucHViZGV2LmF6dXJlLnByb2NvdW50b3IuY29tIiwiaWF0IjoxNzIxMzk1NDA4LCJqdGkiOiJkZmY3ZDdkOS1mNWJmLTRlZTYtYmU1MC1hNTRlZGRiODJhMGIiLCJjaWQiOjE1NTIxfQ.L6DojPNqC4qIduD6D2R-wf0NrKcpcJgMjCdg74hr9MY
ENV DATA_DIRECTORY=./DEP
ENV ACCOUNT_NUMBER=FI6499899900010338
ENV BIC=NDEAFIHH

CMD ["python3", "/app/main.py"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]