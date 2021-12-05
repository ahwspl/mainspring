FROM ubuntu:18.04

MAINTAINER Darshit Kothari <darshit.kothari@ahwspl.com>

RUN apk update; \
    apk add --no-cache gcc musl-dev python3-dev autoconf automake make libffi libffi-dev libxml2-dev libxslt-dev libressl-dev openssl-dev cargo curl git; \
    apk upgrade busybox

RUN apt-get -qq update && \
    apt-get -qq install python-virtualenv git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Upgrade urllib3
RUN pip install --no-cache-dir --upgrade urllib3

RUN virtualenv /mnt/scheduler && \
    . /mnt/scheduler/bin/activate && \
    pip install -e git+https://github.com/darshitkothari/mainspring.git#egg=mainspring && \
    pip install -r /mnt/scheduler/src/mainspring/simple_scheduler/requirements.txt

ADD apns.pem /mnt/scheduler/
ADD run_scheduler /mnt/scheduler/bin/run_scheduler
RUN chmod 755 /mnt/scheduler/bin/run_scheduler

CMD ["/mnt/scheduler/bin/run_scheduler"]