"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from gunicorn.app.base import Application
from gunicorn import util


def max_workers():
    return cpu_count()


class runDHBox(Application):
    '''
    Custom Gunicorn Application
    '''

    def __init__(self, options={}):
        '''__init__ method

        Load the base config and assign some core attributes.
        '''
        self.usage = None
        self.callable = None
        self.options = options
        self.do_load_config()

    def init(self, *args):
        '''init method

        Takes our custom options from self.options and creates a config
        dict which specifies custom settings.
        '''
        cfg = {}
        for k, v in self.options.items():
            if k.lower() in self.cfg.settings and v is not None:
                cfg[k.lower()] = v
        return cfg

    def load(self):
        '''load method

        Imports our application and returns it to be run.
        '''        
        return util.import_app("dhbox:app")
    def prog(self):
    	pass


if __name__ == "__main__":
    options = {
            'bind' : '127.0.0.1:80',
		'max_requests' : 1000,
		'worker_class' : 'gevent',
		'workers' : max_workers(),
    }

    runDHBox(options).run()
