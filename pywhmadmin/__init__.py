__title__ = 'pywhmadmin'
__author__ = 'pokeybill'
__version__ = '0.1.1'
__license__ = 'MIT License'

# Stdlib Includes
import argparse
import sys, os
import traceback
import time
import json
import base64
import inspect

# pywhmadmin modules
import whm
import cpanel
import cpanel2
import scripts
import usage

class ParentApp():

    """ Parent class to contain Error definitions and global conf """

    # GLOBAL Configuration
    LOG_PATH = os.path.expanduser('~/pywhm.log')

    def __init__(self):
        self.APP_PATH = os.path.abspath(inspect.getfile(ParentApp))

        # inits
        self.__init_args__()  # Parse command-line arguments
        self.__init_logs__()  # Instantiate the logger, create files if missing
        self.__init_cache__() # Authenticates if a cpsess is missing

        # input validation
        self._process_inputs() # Validate inputs

    def __init_cache__(self):
        sess_base = '/'.join(self.APP_PATH.split('/')[:-1])
        self.cpsess_cache = os.path.join(sess_base,'cache/cpsess')

        if not os.path.isfile(self.cpsess_cache):
            print cpsess_cache

    def __init_args__(self):
        self.args = self._handle_args()

    def __init_logs__(self):
        self.log = self._spawn_logger()

    def _spawn_logger(self):

        if self.args.debug:
            level = logging.DEBUG
        elif self.args.no_log:
            level = logging.ERROR
        else:
            level = logging.INFO

        logger = logging.getLogger(__name__)
        logger.setLevel(level)

        # Create formatters
        file_formatter = logging.Formatter('%(asctime)s | %(levelname)s :: %(message)s')
        cons_formatter = logging.StreamHandler('%(message)s')

        # Create Handlers
        cons_handler = logging.StreamHandler(sys.stdout)
        cons_handler.setFormatter(cons_formatter)
        logger.addHandler(cons_handler)

        if level < logging.ERROR:
            logpath = PyWHMAdminApp.LOG_PATH
            log_handler = logging.FileHandler(logpath, 'w+')
            log_handler.setFormatter(file_formatter)
            logger.addHandler(log_handler)

        return logger

    def _handle_args(self):
        # Must be overridden
        raise AppError("[!] _handle_args() must be overridden ({})".format(self))

    def execute(self):
        #Must be overridden
        raise AppError("[!] execute() must be overridden ({})".format(self))

class MainApp(ParentApp):

    """ Example/Default Application Class """

    def _handle_args(self):
        # Override _handle_args in the child app to customize
        # or create another parser.
        if ('-v' in sys.argv or '--verbose' in sys.argv):
            desc = usage.verbose_description
            epi = usage.verbose_epilog
        else:
            desc = usage.description
            epi = usage.epilog

        parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description=desc,
                    epilog=epi
                    )

        # Flag section
        parser.add_argument('-d','--debug',action='store_true',
                            help='Enable trace on error')
        parser.add_argument('-s','--silent',action='store_true',
                            help='Disable console output')
        parser.add_argument('-f','--format',action='store_true',
                            help='Format API JSON output')
        parser.add_argument('-v','--verbose',action='store_true',
                            help='Enable verbose messages')
        parser.add_argument('-V','--version',action='store_true',
                            help='Display version information')
        parser.add_argument('-l','--flush-log',action='store_true',
                            help='Clears all entries from the log file')
        parser.add_argument('-t','--test',action='store_true',
                            help='Skips actually making API calls')
        parser.add_argument('-c','--host',default='localhost',
                            help='Specify a remote host to manage (default=localhost)')
        parser.add_argument('-u','--username',default='root',
                            help='Specify a username (default=root)')
        parser.add_argument('-p','--password',
                            help='Specify a password')

        # Parameter section
        parser.add_argument('api',default='whm1',
                            choices=['cpanel1','cpanel2','whm1','scripts'
                            'resetdns','listaccts','domlist','mysqlinfo',
                            'acctsummary'
                            ],
                            help='Specify an api, script, or action')
        parser.add_argument('params',nargs=argparse.REMAINDER,
                            help='Parameter list for the command chosen')
        return parser.parse_args()

    def _process_input(self):
        # Customizing input parsing

        # Require a password for remote management
        if self.args.host != 'localhost':
            if self.args.password is None:
                self.args.password = raw_input(
                                "Password ({})> ".format(self.args.username)
                                )

        


class AppError(AssertionError):

    def __init__(self, msg, fatal=True):
        self.err_cls, self.err, self.raw_trc = sys.exc_info()
        self.trace = traceback.format_tb(self.raw_trc)
        self.msg = msg

    def _log_err(self, logger):
        msg = ['[!] PyWHMAdmin Exception Report\n']
        logger.debug(''.join(msg.extend(self.trace)))

if __name__=='__main__':
    start = time.clock()
    # Direct execution 

    try:
        app = MainApp()
        app.log.info('[*] PyWHMAdmin Execution Started')
        app.execute()
        app.cleanup()
    except AppError as e:
        e._log_err(app.log)
        if e.fatal: raise
    except Exception as e:
        raise
        app.log.exception("[!] Application Error:")
    else:
        app.log.info('[*] Execution Succeeded in {:.3f}s'.format(time.clock()-start))
