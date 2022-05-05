FROM openjdk:slim

COPY --from=python:3.6 / /

COPY . /usr/src/myapp
WORKDIR /usr/src/myapp

ENV PYTHONUNBUFFERED=1
RUN pip3 install --no-cache-dir  --upgrade -r ./requirements.txt
RUN cd /usr/local/sbin
RUN wget https://dlcdn.apache.org/storm/apache-storm-1.2.4/apache-storm-1.2.4.tar.gz
RUN tar xfvz apache-storm-1.2.4.tar.gz
RUN wget https://downloads.apache.org/zookeeper/stable/apache-zookeeper-3.6.3-bin.tar.gz 
RUN tar xfvz apache-zookeeper-3.6.3-bin.tar.gz 
RUN apt-get update && apt-get -y install leiningen
RUN echo export PATH=/usr/local/sbin/apache-storm-2.4.0/bin:/bin:/usr/local/openjdk-17/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin >> ~/.bashrc
RUN echo export LEIN_ROOT=/usr/bin/lein >> ~/.bashrc
# RUN zkServer start
RUN apt-get -y install vim

# RUN ./apache-zookeeper-3.6.3-bin/bin/zkServer.sh start




ENTRYPOINT ["/bin/bash"]