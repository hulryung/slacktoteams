FROM python:latest

COPY app /app
COPY run.sh /run.sh
COPY requirements.txt /requirements.txt

CMD ["/bin/sh", "/run.sh"]