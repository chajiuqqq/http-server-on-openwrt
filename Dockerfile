FROM python:3.6-alpine
WORKDIR /code
VOLUME /root/web:/code
RUN pip install redis flask
CMD ["python", "app.py"]