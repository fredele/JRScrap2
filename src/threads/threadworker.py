#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.network.urlrequest import UrlRequest


class ThreadWorker():
    ThreadsList = []
    resu = []

    def __init__(self, clbk):
        self.EndCallback = clbk
        self.count = 0
        self.ThreadsList = []

    def AddThread(self, name, req, callback):
        self.count += 1
        self.ThreadsList.append({'name': name, 'request': req, 'callback': callback, 'status': 'pending'})

    def Runthreads(self):
        for thread in self.ThreadsList:
            UrlRequest(thread['request'], self.callback)

    def callback(self, req, res):
        self.count -= 1
        for thread in self.ThreadsList:
            if thread['request'] == req.url:
                self.resu.append({'name': thread['name'], 'result': thread['callback'](req, res)})
                thread['status'] = 'success'
        self.terminated()

    def terminated(self):
        if self.count == 0:
            self.EndCallback(self.resu)
            self.resu = []
            self.ThreadsList = []
