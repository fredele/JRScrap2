#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.network.urlrequest import UrlRequest


class ThreadWorker():
    ThreadsList = []
    resu = []

    def __init__(self, clbk):
        self.EndCallback = clbk
        self.count = 0

    def error(self, req):
        self.count -= 1
        for thread in self.ThreadsList:
            if thread['request'] == req.url:
                thread['status'] = 'error'
        self.terminated()

    def failure(self, req):
        self.count -= 1
        for thread in self.ThreadsList:
            if thread['request'] == req.url:
                thread['status'] = 'failure'
        self.terminated()

    def AddThread(self, name, req, callback):
        self.count += 1
        self.ThreadsList.append({'name': name, 'request': req, 'callback': callback, 'status': 'pending'})

    def Runthreads(self):
        for thread in self.ThreadsList:
            UrlRequest(thread['request'], on_success=self.callback, on_error=self.error, on_failure=self.failure)

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
