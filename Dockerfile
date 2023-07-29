FROM python:3.8.16-slim-buster

ARG INCUBATOR_VER=unknown

WORKDIR /opt/NewsCrawlingService
COPY ./requirements.txt /opt/NewsCrawlingService/requirements.txt
# Install Requirement
RUN pip3 install --no-cache-dir -r requirements.txt


ENV TZ="Asia/Ho_Chi_Minh"
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
COPY . /opt/NewsCrawlingService