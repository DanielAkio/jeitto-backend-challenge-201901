#!/bin/bash
app_name='jeitto'
docker build -t ${app_name} .
docker run --env-file=.env -d -p 5000:5000 ${app_name}:latest