FROM python:3.12.2-alpine

WORKDIR /app

RUN pip install "fastapi[all]"

VOLUME ["/app"]
EXPOSE 8000

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]