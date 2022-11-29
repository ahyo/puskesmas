FROM python:3.10.0-slim
WORKDIR /app
COPY . ./app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD ["python", "app.py"]