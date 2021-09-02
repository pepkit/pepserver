FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY ./pepserver /app/app

# dependencies
COPY requirements.txt /
RUN pip install  pip
RUN pip install -r /requirements.txt