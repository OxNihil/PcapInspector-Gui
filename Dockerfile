FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tshark
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /code/
