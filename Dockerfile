FROM python:3
ENV MYSQL_URI='mysql://utbhj4gmmyroc07r:jWrujlu9SHqG49n7v86V@booh3ea84eak40eq7jcp-mysql.services.clever-cloud.com:3306/booh3ea84eak40eq7jcp'
ENV SECRET_KEY='secret_key'
WORKDIR /jeitto
COPY . /jeitto
RUN pip install -r /jeitto/requirements.txt
ENTRYPOINT ["python"]
CMD ["/jeitto/run.py" ]