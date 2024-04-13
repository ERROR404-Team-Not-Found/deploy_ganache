FROM python:3.10-alpine

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip --no-cache-dir install -r requirements.txt
CMD ["python3", "main.py"]