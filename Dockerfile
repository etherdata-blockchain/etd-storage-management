FROM python:3.9
WORKDIR /usr/local/app
COPY storage /usr/local/app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
EXPOSE 80

WORKDIR /usr/local/app/storage
CMD ["gunicorn", "storage.wsgi"]