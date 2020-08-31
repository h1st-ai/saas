FROM python:3.7

EXPOSE 8999

RUN mkdir -p /app
COPY requirements.txt /app/
RUN pip install --no-cache -r /app/requirements.txt
COPY ./restapi /app/restapi
COPY ./h1st_saas /app/h1st_saas
COPY server.sh server.py worker.py /app/


ENV ENVIRONMENT=production \
    PORT=8999

WORKDIR /app
CMD "./server.sh"
