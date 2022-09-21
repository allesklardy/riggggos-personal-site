#!/bin/bash
docker build -t server:latest .
docker run --rm -d -p 4000:4000 server