FROM docker.io/library/python@sha256:188b0c4c0c28abdbae2ceb1e3881abdd78817dbeed9e5dbc8a15cd8d3a0dcca2
#https://github.com/docker-library/repo-info/blob/master/repos/python/remote/3.7-slim-buster.md
#FROM python:3.7-slim-buster

COPY ofwatchdog-ppc64le /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

ARG ADDITIONAL_PACKAGE
# Alternatively use ADD https:// (which will not be cached by Docker builder)

RUN apt-get -qy update && apt-get -qy install gcc make ${ADDITIONAL_PACKAGE}
RUN apt-get -qy install zlib1g-dev libjpeg-dev

# Add non root user
RUN addgroup --system app && adduser app --system --ingroup app
RUN chown app /home/app

USER app

ENV PATH=$PATH:/home/app/.local/bin

WORKDIR /home/app/

COPY index.py .
COPY requirements.txt .

USER root
#RUN python -m pip install -U --force-reinstall pip
RUN pip install -r requirements.txt

# Build the function directory and install any user-specified components
USER app

RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR /home/app/function/
COPY function/requirements.txt .
RUN pip install --user -r requirements.txt

#install function code
USER root

COPY function/ .
RUN chown -R app:app ../

ARG TEST_COMMAND=tox
ARG TEST_ENABLED=true
RUN if [ "$TEST_ENABLED" = "false" ]; then echo "skipping tests"; else eval "$TEST_COMMAND";  fi

WORKDIR /home/app/

#configure WSGI server and healthcheck
USER app

ENV fprocess="python index.py"

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
