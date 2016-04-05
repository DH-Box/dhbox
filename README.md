DH Box
=====

A toolbox for Digital Humanities.

[Wiki](https://github.com/DH-Box/dhbox/wiki)


###DH BOX Local Install Process
Currently DH Box requires a linux that has apt-get.
#### One line install:
```
wget -qO- https://raw.githubusercontent.com/DH-Box/dhbox/master/install_dhbox.sh | sudo sh
```
Edit settings as desired in `config.cfg` and run with `python wsgi.py`.

or:

1. [Install Docker](https://www.docker.com/)
2. Install `pip`, Python package manager
3. Clone git repo (`git clone https://github.com/DH-Box/dhbox.git`)
4. Navigate to `dhbox/` 
5. Run `pip install -r requirements.txt` (preferably in a virtualenv)
6. Navigate to `dhbox/seed` 
7. Run `sudo docker build -t thedhbox/seed:latest .` (takes 15 minutes or more)
8. Navigate to `dhbox/`
9. Edit settings as desired in `config.cfg`
10. Run `manage build_database`
10. Run `python wsgi.py`
11. Navigate to site on `http://localhost:80`

###If you are developing for DH Box, there are a few more steps:

11. Install Node and Node Package Manager: `apt-get install nodejs npm`
12. Install Gulp and Bower: `npm install gulp bower`
13. Changes to the site go into the `/src` directory. Propagate changes with `gulp build`
