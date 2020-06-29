FROM python:3
WORKDIR /jeitto
ENV MYSQL_URI=${MYSQL_URI}
ENV SECRET_KEY=${SECRET_KEY}
COPY . /jeitto
RUN pip install -r /jeitto/requirements.txt
ENTRYPOINT ["python"]
CMD ["/jeitto/run.py" ]