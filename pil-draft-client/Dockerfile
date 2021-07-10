FROM docker.io/library/python@sha256:188b0c4c0c28abdbae2ceb1e3881abdd78817dbeed9e5dbc8a15cd8d3a0dcca2
#https://github.com/docker-library/repo-info/blob/master/repos/python/remote/3.7-slim-buster.md
#FROM python:3.7-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
