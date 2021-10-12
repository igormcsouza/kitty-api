FROM python:3.8-slim

COPY requirements.txt /opt/requirements.txt
RUN pip install pip --upgrade &&\
    pip install -r /opt/requirements.txt

ENV TF_CPP_MIN_LOG_LEVEL=2

WORKDIR /kitty-api
COPY api /kitty-api/api

CMD uvicorn api:app --host 0.0.0.0