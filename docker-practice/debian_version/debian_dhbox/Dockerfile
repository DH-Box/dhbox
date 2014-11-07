FROM steve/seed
MAINTAINER Steve
RUN find . -type f -delete
ADD . /src
RUN apt-get -y update
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# RUN git clone http://github.com/ansible/ansible.git /tmp/ansible
# WORKDIR /tmp/ansible
# ENV PATH /tmp/ansible/bin:/sbin:/usr/sbin:/usr/bin:/bin/
# ENV ANSIBLE_LIBRARY /tmp/ansible/library
# ENV PYTHONPATH /tmp/ansible/lib:$PYTHON_PATH
# ADD hosts /etc/ansible/hosts
WORKDIR /src
RUN ansible-playbook start.yml -c local
EXPOSE 22 8787 80 4200
CMD ["/usr/bin/supervisord"]