FROM python:3.13-alpine

WORKDIR /app

RUN pip install "fastapi[all]"

VOLUME ["/app/api"]
EXPOSE 8000

COPY setup.py pyproject.toml .
RUN pip install -e .

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

ARG VCS_VERSION
ENV VCS_VERSION=${VCS_VERSION}

COPY main.py .

CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
