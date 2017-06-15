import threading
import time
from kivy.app import App


class FuncDelay(threading.Thread):

    def __init__(self,  timeout, val):
        threading.Thread.__init__(self)
        self.val = val
        self.timeout = timeout
        self.app = App.get_running_app()

    def run(self):
        time.sleep(self.timeout)
        self.app.FieldsStackWidget.imagefield.SetMCImage(self.val)
