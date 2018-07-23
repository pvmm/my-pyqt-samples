# coding: utf-8
import sys

class StdoutLogger:
    sys.stderr = sys.stdout

    @staticmethod
    def debug(msg):
        print(msg)
        
    @staticmethod
    def info(msg):
        print(msg)
    
    @staticmethod
    def error(msg):
        print(msg)
        
    @staticmethod
    def critical(msg):
        print(msg)
        
    @staticmethod
    def warning(msg):
        print(msg)

    @staticmethod
    def trace(msg):
        print(msg)

