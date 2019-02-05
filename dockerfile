FROM python:latest

COPY src /app

COPY requirements.txt /

RUN pip install -r requirements.txt


WORKDIR /app

#ENTRYPOINT  ["python"]

CMD python -u data_dump.py && python -u app.py

