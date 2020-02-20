# author: Sam Edwardes
# date: 2020-02-04
# BUILD:
#   docker build --tag jrescribetranscripts .
# RUN CONTAINER AND OPEN BASH:
#   docker run -it --rm jrescribetranscripts bin/bash
FROM python

RUN pip install --upgrade pip
RUN pip install --no-cache-dir pandas

RUN apt-get update
RUN apt-get install tree
RUN apt-get install -y python-dev 

# POCKETSPHINX
# https://pypi.org/project/pocketsphinx/
# Make sure we have up-to-date versions of pip, setuptools and wheel
RUN python -m pip install --upgrade pip setuptools wheel
RUN apt-get install -y swig 
RUN apt-get install -y python python-dev python-pip build-essential swig git libpulse-dev
# RUN pip install --upgrade --no-cache-dir pocketsphinx

# REFERENCE
# https://gist.github.com/AlekseiCherkes/8e8b9cd2dd22cceb77a0#file-dockerfile-sphinx
