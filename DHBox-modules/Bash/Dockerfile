FROM dhbox/seed
MAINTAINER Steve

ADD . /src
#RUN apt-get -y update

# Set correct environment variables.
ENV HOME /root

#Adding Deamons to containers
RUN mkdir -p /etc/service/rserver
RUN mv /src/runit_scripts/rserver.sh /etc/service/rserver/run
RUN chmod +x /etc/service/rserver/run

RUN mkdir -p /etc/service/mysql
RUN mv /src/runit_scripts/mysql.sh /etc/service/mysql/run
RUN chmod +x /etc/service/mysql/run

RUN mkdir -p /etc/service/apache2
RUN mv /src/runit_scripts/apache2.sh /etc/service/apache2/run
RUN chmod +x /etc/service/apache2/run

RUN mkdir -p /etc/service/shellinabox
RUN mv /src/runit_scripts/shellinabox.sh /etc/service/shellinabox/run
RUN chmod +x /etc/service/shellinabox/run

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]


EXPOSE 22 8787 80 4200

##startup script
#Pre-config script that needs to be run once, when the container runs for the first time
RUN mkdir -p /etc/my_init.d
COPY tmp/startup.sh /etc/my_init.d/startup.sh
RUN chmod +x /etc/my_init.d/startup.sh

