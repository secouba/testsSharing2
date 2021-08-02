FROM python:3.8
RUN apt-get update \
&& apt-get install -y git \
&& apt-get -y upgrade \
&& mkdir /code \
&& cd /code
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt
#RUN git clone https://github.com/secouba/testsSharingCloud.git /code