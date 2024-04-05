FROM python:3.10

WORKDIR /app

RUN wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY app.py ./

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
