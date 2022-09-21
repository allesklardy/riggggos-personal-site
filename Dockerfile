FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash nano
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
ENV LISTEN_PORT=4000
EXPOSE 4000
RUN pip install -r requirements.txt
COPY . /app
ARG MY_MAIL_PASSWORD
ENV MY_MAIL_PASSWORD $MY_MAIL_PASSWORD
ENTRYPOINT [ "python" ]
CMD ["server.py"]