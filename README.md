DH Box
=====

A toolbox for Digital Humanities.

###DH BOX Local Install Process
Currently DH Box requires Ubuntu >= 14.04 and Python 2.7x
### One line install:
```
wget -qO- https://raw.githubusercontent.com/DH-Box/dhbox/master/install_dhbox.sh | sudo sh
```
1. Navigate to `dhbox/` 
2. Rename `config.cfg.template` to `config.cfg` and edit settings as desired
3. Run `sudo python manage.py build_database`
4. Run `sudo python wsgi.py`
5. Navigate to site on `http://localhost:80`

####Or for a manual install:

1. [Install Docker](https://www.docker.com/)
2. Install `pip`, Python package manager
3. Clone git repo (`git clone https://github.com/DH-Box/dhbox.git`)
4. Navigate to `dhbox/` 
5. Run `pip install -r requirements.txt` (preferably in a virtualenv)
6. Rename `config.cfg.template` to `config.cfg` and edit settings as desired
7. Run `sudo manage start` to download the DH Box seed, or navigate to `dhbox/seed` and run `docker build -t thedhbox/seed:latest .` if you want to build it yourself (takes 15 minutes or more).
8. Run `sudo manage build_database`
9. Run `sudo python wsgi.py`
10. Navigate to site on `http://localhost:80`

###If you are developing for DH Box, there are a few more steps:

11. Install Node and Node Package Manager: `apt-get install nodejs npm`
12. Install Gulp and Bower: `npm install gulp bower`
13. Changes to the site go into the `/src` directory. Propagate changes with `gulp build`
