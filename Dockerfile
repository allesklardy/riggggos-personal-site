FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash nano
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
ENV LISTEN_PORT=4000
EXPOSE 4000
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python" ]
CMD ["server.py"]