#!/usr/bin/python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

#Font: https://stackoverflow.com/questions/2124190/how-do-i-implement-interfaces-in-python

class XInterface(object):
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"
    @abstractmethod
    def getDownloadLink(self,value): raise NotImplementedError
    @abstractmethod
    def getSearchResults(self,value): raise NotImplementedError