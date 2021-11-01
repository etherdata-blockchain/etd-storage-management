FROM python:3.9
WORKDIR /usr/local/app
COPY . .
#COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
EXPOSE 8000

WORKDIR /usr/local/app/storage

CMD ["gunicorn", "storage.wsgi"]