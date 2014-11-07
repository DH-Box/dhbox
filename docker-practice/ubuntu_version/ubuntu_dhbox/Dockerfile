FROM steve/seed
MAINTAINER Steve
#RUN find . -type f -delete
ADD . /src
RUN apt-get -y update
WORKDIR /src
RUN ansible-playbook start.yml -c local
EXPOSE 22 8787 80 4200

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

#Adding Deamons to containers
RUN mkdir -p /etc/service/rserver
RUN mv /src/runit_scripts/rserver.sh /etc/service/rserver/run
RUN chmod +x /etc/service/rserver/run
RUN ln -s /etc/apparmor.d/rstudio-server /etc/apparmor.d/disable/

RUN mkdir -p /etc/service/mysql
RUN mv /src/runit_scripts/mysql.sh /etc/service/mysql/run
RUN chmod +x /etc/service/mysql/run

RUN mkdir -p /etc/service/apache2
RUN mv /src/runit_scripts/apache2.sh /etc/service/apache2/run
RUN chmod +x /etc/service/apache2/run

RUN mkdir -p /etc/service/shellinabox
RUN mv /src/runit_scripts/shellinabox.sh /etc/service/shellinabox/run
RUN chmod +x /etc/service/shellinabox/run