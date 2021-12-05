FROM ubuntu:18.04

MAINTAINER Darshit Kothari <darshit.kothari@ahwspl.com>

RUN apt-get -qq update && \
    apt-get -qq install python-virtualenv git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN virtualenv /mnt/scheduler && \
    . /mnt/scheduler/bin/activate && \
    pip install -e git+https://github.com/darshitkothari/mainspring.git#egg=mainspring && \
    pip install -r /mnt/scheduler/src/mainspring/simple_scheduler/requirements.txt

ADD apns.pem /mnt/scheduler/
ADD run_scheduler /mnt/scheduler/bin/run_scheduler
RUN chmod 755 /mnt/scheduler/bin/run_scheduler

CMD ["/mnt/scheduler/bin/run_scheduler"]
