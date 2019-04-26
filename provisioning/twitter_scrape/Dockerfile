FROM python:3.7.3

WORKDIR /mnt/src
# because docker caches each new line of command, we should add new packages one per new line to avoid long image rebuilds
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y nano git

# for graceful shutdown
RUN pip install honcho

# requirements
RUN pip install flask==0.12.4
RUN pip install gunicorn==19.9.0
RUN pip install requests==2.21.0
RUN pip install beautifulsoup4==4.7.1
RUN pip install tzlocal==1.5.1

ADD start_server.sh /mnt/start_server.sh

VOLUME ["/var/log/"]
VOLUME ["/mnt/src/"]
CMD ["/mnt/start_server.sh"]
