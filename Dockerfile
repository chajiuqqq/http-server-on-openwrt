FROM python:3.6-alpine
# COPY . /code
# VOLUME /root/web:/code
RUN echo -e "nameserver 114.114.114.114\nnameserver 8.8.8.8" >> /etc/resolv.conf \
    && pip install redis flask
WORKDIR /code
# CMD ["python", "app.py"]