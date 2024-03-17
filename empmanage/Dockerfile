FROM --platform=$BUILDPLATFORM python:3.11.6-slim AS builder
ENV PYTHONUNBUFFERED=1

EXPOSE 8000


WORKDIR /app


RUN apt-get update \
    && apt-get install python3-dev default-libmysqlclient-dev gcc pkg-config -y


COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
RUN pip3 install django-debug-toolbar
RUN pip3 install django-cors-headers

COPY . /app 
# ENTRYPOINT ["python3"] 
# CMD ["manage.py", "runserver", "0.0.0.0:8000"]
