FROM phusion/baseimage:0.9.16
MAINTAINER Steve

# Set correct environment variables.
ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive

ENV REFRESHED_AT 2015-04-02

RUN echo "deb http://cran.rstudio.com/bin/linux/ubuntu trusty/" >> /etc/apt/sources.list
RUN apt-get -y update

# General needs
RUN apt-get -qy install git python-apt apt-utils python-pip python-dev sudo curl git wget unzip python-pip opensmtpd ipython-notebook nodejs npm
RUN pip install PyYAML jinja2 paramiko

# For Shellinabox
RUN apt-get -y install shellinabox
ADD ./shellinabox /etc/default/

# For MALLET
RUN apt-get -qy install default-jdk ant
RUN mkdir /mallet
RUN wget -O /tmp/mallet.tar.gz http://mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz
RUN tar xfz /tmp/mallet.tar.gz --strip-components=1 -C /mallet
RUN ant -buildfile /mallet/build.xml

# For NLTK
RUN apt-get -qy install python-numpy python-scipy python-matplotlib 
RUN pip install NLTK

# For R-Studio
RUN apt-get -qy --force-yes install r-base r-base-dev gdebi-core libatlas3-base libapparmor1 apparmor-profiles libssl0.9.8
RUN wget http://download2.rstudio.org/rstudio-server-0.98.501-amd64.deb -O rstudio.deb
RUN yes | gdebi rstudio.deb
RUN ln -s /etc/apparmor.d/rstudio-server /etc/apparmor.d/disable/

# For Omeka
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd 
RUN apt-get -qy install apache2 php5 rsync mysql-server php5-mysql imagemagick python-mysqldb
RUN mkdir -p /var/www/omeka/
RUN wget -O /tmp/omeka.zip http://omeka.org/files/omeka-2.3.zip
RUN unzip -qo /tmp/omeka.zip -d /var/www/omeka/
RUN cp -r /var/www/omeka/omeka-2.3/* /var/www/omeka/
RUN cp -r /var/www/omeka/omeka-2.3/.htaccess /var/www/omeka/
RUN rm -rf /var/www/omeka/omeka-2.3/
RUN chown -R www-data /var/www
RUN chgrp -R www-data /var/www
RUN echo "cgi.fix_pathinfo=0" > etc/php5/apache2/conf.d/10-fix_pathinfo.ini

# weird database stuff
# RUN service mysql start
# RUN mysqld_safe &
# RUN mysql -uroot -e "DROP USER omeka@localhost;"
# RUN sleep 5
# RUN mysql -uroot -e "CREATE USER 'steve'@'LOCALHOST' IDENTIFIED BY 'tsest'"

ADD . /src
# Install ansible
RUN pip install ansible==1.7

RUN mkdir -p /etc/ansible/
RUN echo "[local]" > /etc/ansible/hosts
RUN echo "localhost ansible_connection=local" >> /etc/ansible/hosts
WORKDIR /src
RUN ansible-playbook start.yml -v -c local

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

RUN mkdir -p /etc/service/smtpd
RUN mv /src/runit_scripts/smtpd.sh /etc/service/smtpd/run
RUN chmod +x /etc/service/smtpd/run

EXPOSE 22 25 8787 80 4200

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]