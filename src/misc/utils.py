#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import datetime

dateformat = "%d/%m/%Y"

# In Python 2, a string may be of type str or of type unicode.


def HTTPToSTR(val):
    r = val
    if isinstance(val, unicode):
        # unicode may contain ascii chars
        r = (urllib.unquote(val)).encode("utf-8")
    elif isinstance(val, int):
        r = (urllib.unquote(str(val))).encode("utf-8")
    elif isinstance(val, str):
        r = val
    return r


def STRToHTTP(val):
    r = val
    if isinstance(val, str):
        r = urllib.quote(val)
    elif isinstance(val, unicode):
        # unicode may contain ascii chars
        r = urllib.quote(val.encode("utf-8"))
    return r


def DateToExcel(strdate, dateformat):
    date = datetime.datetime.strptime(strdate, dateformat)
    temp = datetime.datetime(1899, 12, 30)
    r = date-temp
    return str(r.days)


def ExcelToDate(xldate, dateformat):
    temp = datetime.datetime(1899, 12, 30)
    delta = datetime.timedelta(days=int(xldate))
    date = temp+delta
    return str(date.strftime(dateformat))


def StrFindBetween(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""
