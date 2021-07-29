FROM ibmcom/powerai:1.7.0-tensorflow-cpu-ubuntu18.04-py37-ppc64le
#FROM ibmcom/powerai:1.7.0-base-ubuntu18.04-py37
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV http_proxy=http://10.3.0.3:3128
ENV https_proxy=http://10.3.0.3:3128

LABEL maintainer="Alexei Karve <karve@us.ibm.com>"

RUN sudo install -g pwrai -o pwrai -d /workspace
WORKDIR /workspace
RUN mkdir assets

# Dependencies for building NumPy and Pillow (Prebuilt NumPy and Pillow are not available for ppc)
RUN sudo http_proxy=$http_proxy https_proxy=$https_proxy apt-get update && sudo http_proxy=$http_proxy https_proxy=$https_proxy apt-get install -y \
      build-essential \
      # NumPy
      gfortran \
      libblas-dev \
      liblapack-dev \
      # Pillow
      libjpeg-dev \
      zlib1g-dev \
      && sudo rm -rf /var/lib/apt/lists/*

# Cython is required for building NumPy
RUN ["/bin/bash", "-c", "cd /opt/anaconda/bin && source activate wmlce && pip install --upgrade pip && pip install Cython --install-option='--no-cython-compile'" ]

# The following is required to get flask to work with the version of werkzeug (0.14) available in PowerAI
RUN ["/bin/bash", "-c", "cd /opt/anaconda/bin && source activate wmlce && pip install flask-cors==3.0.10 flask-restx==0.5.0 flask=='1.1.4,<2.0' maxfw==1.1.6 numpy==1.18.5"]

# this is needed for tesseract versions prior to 4.1 (https://github.com/tesseract-ocr/tesseract/issues/1670#issuecomment-515324015)
ENV LC_ALL=C
RUN sudo http_proxy=$http_proxy https_proxy=$https_proxy apt-get update \
     && sudo http_proxy=$http_proxy https_proxy=$https_proxy apt-get install -y \
         tesseract-ocr \
         libtesseract-dev \
         libleptonica-dev \
         pkg-config \
         gcc \
         g++ \
     && sudo rm -rf /var/lib/apt/lists/*
RUN ["/bin/bash", "-c", "cd /opt/anaconda/bin && source activate wmlce && pip install tesserocr"]

COPY app.py .
COPY app.sh .
COPY api api
COPY core core
COPY static static
COPY config.py .

USER root

COPY ofwatchdog-ppc64le /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog
USER pwrai

ENV fprocess='/workspace/app.sh'
# Set to true to see request in function logs
ENV write_debug="true"
ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
