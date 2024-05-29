FROM python:3.11-slim
WORKDIR /app
COPY ./requirements.txt requirements.txt 
RUN python3.11 -m pip install -r requirements.txt
COPY ./app ./app