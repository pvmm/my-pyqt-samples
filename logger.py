# coding: utf-8
import sys, os


class StdoutLogger:
    sys.stderr = sys.stdout
    _loglevel = [] if 'RELEASE' in os.environ else ['DEBUG', 'INFO', 'WARNING', 'ERROR']


    @classmethod
    def loglevel(cls, self):
        return cls._loglevel


    @classmethod
    def loglevel(cls, *loglevels):
        cls._loglevel = loglevels


    @classmethod
    def debug(cls, msg):
        if 'DEBUG' in cls._loglevel:
            print('[DEBUG] %s' % msg)
        

    @classmethod
    def info(cls, msg):
        if 'INFO' in cls._loglevel:
            print('[INFO] %s' % msg)
    

    @classmethod
    def error(cls, msg):
        if 'ERROR' in cls._loglevel:
            print('[ERROR] %s' % msg)


    @classmethod
    def critical(cls, msg):
        print('[CRITICAL] %s' % msg)
        exit()
        

    @classmethod
    def warning(cls, msg):
        if 'WARNING' in cls._loglevel:
            print('[WARNING] %s' % msg)


    @classmethod
    def trace(cls, msg):
        print('[TRACE] %s' % msg)

