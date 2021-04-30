FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY tcp-server.py ./

ENTRYPOINT ["python3", "-u", "/tcp-server.py"]
