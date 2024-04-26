FROM python:3.11-alpine
WORKDIR /proj
COPY ./requirements.txt requirements.txt 
RUN python3.11 -m pip install -r requirements.txt
COPY ./ ./