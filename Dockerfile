FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN echo "nameserver 10.202.10.202" > /etc/resolv.conf

COPY . /app/

EXPOSE 8000

CMD ["python3", "main.py"]
