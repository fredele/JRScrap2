#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger
from kivy.app import App
from misc.fields import New_Fields
from misc.utils import ExcelToDate, DateToExcel, STRToHTTP
from modal.noauthenticate import NoConnection
from misc.funcdelay import FuncDelay
import base64
import urllib
from misc.utils import StrFindBetween

import xml.etree.ElementTree as ET


class MCWS():
    headers = {}
    address = ''
    port = ''
    address1 = ''
    address2 = ''
    Token = None

    def __init__(self, address=None, port=None):
        self.app = App.get_running_app()
        if ((address is not None) and (port is not None)):
            MCWS.address = address
            MCWS.port = port
            MCWS.address1 = 'http://'+str(MCWS.address)+':'+str(MCWS.port)+'/MCWS/v1/'
            MCWS.address2 = 'http://'+str(MCWS.address)+':'+str(MCWS.port)+'/'

    def RESTToDict(self, res):
        res_dict = dict()
        root = ET.fromstring(res.encode('utf-8'))
        res_dict['Status'] = root.attrib['Status']
        for child in root:
            res_dict[str(child.attrib['Name'])] = child.text
        return res_dict

    def MPLToDict2(self, res):
        root = ET.fromstring(res.encode('utf-8'))
        res_dict = dict()
        for child in root[0]:
            res_dict[str(child.attrib['Name'])] = child.text
        return res_dict

    def MPLToDict(self, res):
        root = ET.fromstring(res.encode('utf-8'))
        res_dict = dict()
        res = []
        for item in root:
            res_dict = {}
            for child in item:
                res_dict[str(child.attrib['Name'])] = child.text
            res.append(res_dict)
        return res

    def MCWScorrectdisplay(self, field, value):
        r = value
        if field != 'Description':
            r = value.replace('; ', '\n')
        if field == 'Date':
            r = ExcelToDate(value, self.app.DateFormat)
        return r

    def MCWScorrectsave(self, field, value):
        r = value
        if field != 'Description':
            r = value.replace('\n', '; ')
        if field == 'Date':
            r = DateToExcel(value, self.app.DateFormat)
        return r

    def Authenticate(self):
        Logger.debug('Authenticate:Do Authenticate ...')
        url = MCWS.address1+'Authenticate'

        auth = 'Basic ' + base64.b64encode(self.app.config.getdefault("MCWS", "admin", "admin")+':'+self.app.config.getdefault("MCWS", "password", "password"))
        Logger.debug('Authenticate auth:'+auth)
        MCWS.headers = {
                        'Authorization': auth,
                        'Accept': '*/*'
                       }
        UrlRequest(url, req_headers=MCWS.headers, on_success=self.Authenticate_Success, on_error=self.Authenticate_Error, on_failure=self.Authenticate_Failure)

    def Authenticate_Success(self, req, res):
        Logger.debug('Authenticate:Success')
        self.app.MCWS.CreateMCFields()
        dic = self.RESTToDict(res)
        self.Token = str(dic['Token'])
        print('Token:'+self.Token)
        search = self.app.searches[0]["search"]
        self.app.FilesStackWidget.SearchFiles(search)


    def Authenticate_Error(self, req, res):
        Logger.debug('Authenticate:Error')
        Logger.debug(res)
        view = NoConnection()
        view.open()

    def Authenticate_Failure(self, req, res):
        Logger.debug('Authenticate:Failure')
        Logger.debug(res)

# CreateFields
# --------

    def CreateMCField(self, field):
        url = MCWS.address1+"Library/CreateField?Type=string&Name=" + urllib.quote(field) + ""
        UrlRequest(url, req_headers=MCWS.headers, on_success=self.CreateMCField_CallBack)

    def CreateMCFields(self):
        for key in New_Fields:
            self.CreateMCField(key)

    def CreateMCField_CallBack(self, req, res):
        Logger.debug('CreateMCField:NewField')

# Playback
# --------

    def PlayPause(self, callback):
        Logger.debug('Playback:PlayPause')
        UrlRequest(MCWS.address1+'Playback/PlayPause?Zone=-1&ZoneType=ID', req_headers=MCWS.headers, on_success=callback)

    def Pause(self, callback):
        Logger.debug('Playback:Pause')
        UrlRequest(MCWS.address1+'Playback/Pause?State=-1&Zone=-1&ZoneType=ID', req_headers=MCWS.headers, on_success=callback)

    def Next(self, callback):
        Logger.debug('Playback:Next')
        UrlRequest(MCWS.address1+'Playback/Next?Zone=-1&ZoneType=ID', req_headers=MCWS.headers, on_success=callback)

    def Previous(self, callback):
        Logger.debug('Playback:Previous')
        UrlRequest(MCWS.address1+'Playback/Previous?Zone=-1&ZoneType=ID', req_headers=MCWS.headers, on_success=callback)

    def Stop(self, callback):
        Logger.debug('Playback:Stop')
        UrlRequest(MCWS.address1+'Playback/Stop?Zone=-1&ZoneType=ID', req_headers=MCWS.headers, on_success=callback)

    def Info(self, callback):
        UrlRequest(MCWS.address1+'Playback/Info?Zone=-1', req_headers=MCWS.headers, on_success=callback)

    def Current(self, callback):
        url = MCWS.address1+'Files/Current?Action=mpl&ActiveFile=-1&Zone=-1&ZoneType=ID'
        UrlRequest(url, req_headers=MCWS.headers, on_success=callback)

    def SearchFiles(self, query, callback):
        Logger.debug('Search:SearchFiles')
        url = MCWS.address1+'Files/Search?Query='+query
        UrlRequest(url, req_headers=MCWS.headers, on_success=callback)

    def FileInfo(self, key, callback):
        UrlRequest(MCWS.address1+'File/GetInfo?File=' + key, req_headers=MCWS.headers, on_success=callback)

    def SetInfo(self, Filekey, field, value, callback):
        url = MCWS.address1 + 'File/SetInfo?FileType=Key&File=' + STRToHTTP(Filekey)+'&Field=' + STRToHTTP(field) + '&Value=' + STRToHTTP(self.MCWScorrectsave(field, value))
        UrlRequest(url, req_headers=MCWS.headers, on_success=callback, on_error=self.SetInfoError)

    def SetInfoError(self, r, q):
        print('SetInfoError')

    def SetImage(self, key, imageURL):
        u = urllib.urlopen(imageURL)
        raw_data = u.read()
        res = raw_data.encode("base64")
        url = MCWS.address1 + 'File/SetImage?File=' + key+'&FileType=Key&Type=jpg&Image=' + str((res).replace('\n', ''))
        UrlRequest(url, req_headers=MCWS.headers, on_success=self.SetImage_CallBack, on_failure=self.SetImage_CallBack2)

    def SetImage_CallBack(self, req, res):
        if hasattr(self.app.FieldsStackWidget, 'imagefield'):
            # TODO delay this ...
            t = FuncDelay(1, StrFindBetween(req.url, "File=", "&FileType"))
            t.start()
            pass

    def SetImage_CallBack2(self, req, res):
        pass

    def Status(self, req, res):
        pass

    def SetInfo_CallBack(self, req, res):
        pass

    def Info_CallBack(self, req, res):
        res_dict = self.RESTToDict(res)
        self.app.PlayerScreen.ids.player_album.text = res_dict['Album']
        self.app.PlayerScreen.ids.player_title.text = res_dict['Name']
        self.app.PlayerScreen.ids.player_artist.text = res_dict['Artist']
        self.app.PlayerScreen.ids.player_song_elapsed_time.text = res_dict['ElapsedTimeDisplay']
        self.app.PlayerScreen.ids.player_song_total_time.text = res_dict['TotalTimeDisplay']
        self.app.PlayerScreen.ids.player_genre.text = ''
        self.app.PlayerScreen.ids.player_cover.source = MCWS.address2 + res_dict['ImageURL'] + '&Token=' + self.Token
        self.app.PlayerScreen.ids.player_slider.max = int(res_dict['DurationMS'])
        self.app.PlayerScreen.ids.player_slider.value = int(res_dict['PositionMS'])
