FROM python:3.9-slim-buster as base

RUN mkdir -p /usr/src/traffic_app

WORKDIR /usr/src/traffic_app

RUN apt update -y &&\ 
    apt install curl -y

COPY . /usr/src/traffic_app

RUN pip install -r /usr/src/traffic_app/requirements.txt &&\
    chmod +x ./docker-entrypoint.sh &&\
    chmod +x ./docker-entrypoint-test.sh 

FROM base as local

# run app via a shell script 
CMD ["./docker-entrypoint.sh"]

FROM base as test

CMD ["./docker-entrypoint-test.sh"]