FROM python:3.13-alpine

WORKDIR /api

RUN pip install "fastapi[all]"

VOLUME ["/api"]
EXPOSE 8000

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

ARG VCS_VERSION
ENV VCS_VERSION=${VCS_VERSION}

CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
