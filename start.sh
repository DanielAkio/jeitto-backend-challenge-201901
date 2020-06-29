#!/bin/bash
docker build -t jeitto .
docker run -d -p 5000:5000