FROM python:3.9
WORKDIR /usr/local/app
COPY . .
#COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
EXPOSE 8000

WORKDIR /usr/local/app/storage

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:80"
CMD ["gunicorn", "storage.wsgi"]
#CMD ["python", "manage.py", "runserver"]