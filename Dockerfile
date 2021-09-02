FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8
LABEL authors="Nathan LeRoy, Michal Stolarczyk, Nathan Sheffield"

COPY . /app
RUN pip install .