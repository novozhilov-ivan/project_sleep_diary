FROM python:3.10-slim-bookworm
LABEL authors="ivan"

WORKDIR /sleep_diary

COPY requirements.txt .

RUN pip install --upgrade pip -r  requirements.txt

COPY run.py .
COPY app ./app

ENTRYPOINT ["python", "run.py"]