FROM python:3
WORKDIR /jeitto
COPY . /jeitto
RUN pip install -r /jeitto/requirements.txt
ENTRYPOINT ["python"]
CMD ["/jeitto/run.py" ]