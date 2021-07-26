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

 #The following is required to get flask to work with the version of werkzeug (0.14) available in PowerAI
RUN ["/bin/bash", "-c", "cd /opt/anaconda/bin && source activate wmlce && pip install flask-cors==3.0.10 flask-restx==0.5.0 flask=='1.1.4,<2.0' maxfw==1.1.6 numpy==1.18.5"]
# Jinja2-2.11.3 MarkupSafe-2.0.1 Pillow-8.3.1 aniso8601-9.0.1 attrs-21.2.0 click-7.1.2 flask-1.1.4 flask-cors-3.0.10 flask-restx-0.5.0 importlib-metadata-4.6.1 itsdangerous-1.1.0 jsonschema-3.2.0 maxfw-1.1.6 numpy-1.18.5 pyrsistent-0.18.0 pytz-2021.1 typing-extensions-3.10.0.0 zipp-3.5.0

ARG model_bucket=https://max-cdn.cdn.appdomain.cloud/max-object-detector/1.0.2
#ARG model='ssd_mobilenet_v1'
ARG model='faster_rcnn_resnet101'
ARG model_file=${model}.tar.gz
ARG data_file=data.tar.gz
ARG use_pre_trained_model=true

RUN if [ "$use_pre_trained_model" = "true" ] ; then\
    wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=assets/${model_file} && \
           tar -x -C assets/ -f assets/${model_file} -v && ls assets && rm -f assets/${model_file} && \
    wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${data_file} --output-document=assets/${data_file} && \
           tar -x -C assets/ -f assets/${data_file} -v && ls assets && rm -f assets/${data_file}; fi

COPY app.py .
COPY app.sh .
COPY config.py.in .
COPY api api
COPY core core
COPY protos protos
COPY utils utils

# Template substitution: Replace @model@ with the proper model name
RUN sed s/@model@/${model}/ config.py.in > config.py

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
