FROM python:3.8-slim

WORKDIR /kitty-api

COPY requirements.txt /kitty-api/requirements.txt
RUN pip install pip --upgrade &&\
    pip install -r requirements.txt

ENV TF_CPP_MIN_LOG_LEVEL=2

COPY api /kitty-api/api

CMD uvicorn api:app --host 0.0.0.0 --port $PORT