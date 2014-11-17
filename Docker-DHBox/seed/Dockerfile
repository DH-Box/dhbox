FROM phusion/baseimage:0.9.15
MAINTAINER Steve

# Set correct environment variables.
ENV HOME /root

RUN apt-get -y update
RUN apt-get -qy install git python-apt apt-utils python-pip python-dev
RUN pip install PyYAML jinja2 paramiko
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd 
ADD . /src

# Install ansible
RUN pip install ansible==1.7

RUN mkdir -p /etc/ansible/
RUN echo "[local]" > /etc/ansible/hosts
RUN echo "localhost ansible_connection=local" >> /etc/ansible/hosts
WORKDIR /src
RUN ansible-playbook start.yml -c local

EXPOSE 22 8787 80 4200

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]