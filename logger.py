# coding: utf-8
import sys


class StdoutLogger:
    sys.stderr = sys.stdout
    _loglevel = ['DEBUG', 'ERROR']


    @classmethod
    def loglevel(cls, self):
        return cls._loglevel


    @classmethod
    def loglevel(cls, *loglevels):
        cls._loglevel = loglevels


    @classmethod
    def debug(cls, msg):
        if 'DEBUG' in cls._loglevel:
            print(msg)
        

    @classmethod
    def info(cls, msg):
        if 'INFO' in cls._loglevel:
            print(msg)
    

    @classmethod
    def error(cls, msg):
        if 'ERROR' in cls._loglevel:
            print(msg)
        

    @classmethod
    def critical(cls, msg):
        print(msg)
        exit()
        

    @classmethod
    def warning(cls, msg):
        if 'WARNING' in cls._loglevel:
            print(msg)


    @classmethod
    def trace(cls, msg):
        print(msg)

