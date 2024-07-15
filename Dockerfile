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


CMD ["python3", "/app/main.py"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]