FROM python:3.7.4-alpine3.10
RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools
RUN pip3 install pendulum service_identity
ENV TZ="Asia/Kolkata"
RUN mkdir /app
WORKDIR /app
RUN pip install PyMySQL
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY app /app
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]
