FROM python:3.10.8 AS build
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt --no-cache-dir --disable-pip-version-check

 FROM python:3.10.8-slim-bullseye
WORKDIR /app

COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY / ./

ENV PYTHONPATH=/usr/local/lib/python3.10/site-packages
ENTRYPOINT [ "python", "-m","main" ]