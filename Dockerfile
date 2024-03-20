FROM python:3.12.2-alpine

WORKDIR /api

RUN pip install "fastapi[all]"

VOLUME ["/api"]
EXPOSE 8000

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]