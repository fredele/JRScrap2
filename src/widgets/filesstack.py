from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
from widgets.thumbnail import ThumbnailCheckWidget
from widgets.tiles import TilesCheckWidget
from widgets.base import BaseWidget
from kivy.storage.jsonstore import JsonStore


class FilesStackWidget(Widget):
    stack = ObjectProperty()

    def __init__(self, **kwargs):
        super(FilesStackWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.actual_page_number = 0
        self.page_numbers = 0


    def Clear(self):
        self.stack.clear_widgets()

    def AddWidget(self, widget):
        self.stack.add_widget(widget)

    def GetCurrentSelectedFiles(self):
        self.app.MCWS.Current(self.SearchFiles_CallBack)

    def SearchFiles(self, query):
        self.ids.stack.clear_widgets()
        self.app.FilesStackWidget.Clear()
        self.app.MCWS.SearchFiles(query, self.SearchFiles_CallBack)

    def SearchFiles_CallBack(self, req, res):
        self.Clear()
        self.res = self.app.MCWS.MPLToDict(res)
        self.items_count = len(self.res)
        self.page_numbers = self.items_count / int(self.app.filesperpage)
        if self.items_count % int(self.app.filesperpage):
            self.page_numbers += 1
        self.display_widgets()

    def display_widgets(self):
        self.app.FilesStackWidget.Clear()
        if (self.app.store.exists('FileZoom') and (self.app.style == "Thumbnail")):
            self.app.FilesStackScreen.size_slider.value = self.app.store.get(self.app.style + "Zoom")['value']
        firstitemnbr = self.actual_page_number * int(self.app.filesperpage)
        lastitemnbr = min((self.actual_page_number * int(self.app.filesperpage)) + int(self.app.filesperpage), self.items_count)
        self.app.FilesStackScreen.pagenumber.text = "( " + str(self.actual_page_number+1) + " / " + str(self.page_numbers)+" )"
        for i in range(firstitemnbr, min(lastitemnbr, self.items_count)):
            if self.app.style == 'Thumbnail':
                Widget1 = ThumbnailCheckWidget(self.app.FilesStackWidget, self.res[i])
            elif self.app.style == 'Tile':
                Widget1 = TilesCheckWidget(self.app.FilesStackWidget, self.res[i])
            self.AddWidget(Widget1)

    def SetWidgetsSize(self, value):
        for widget in self.stack.walk():
            if isinstance(widget, BaseWidget):
                widget.SetSize(value)

    def SelectInvert(self):
        for widget in self.stack.walk():
            if isinstance(widget, BaseWidget):
                widget.checkbox.active = not widget.checkbox.active

    def SelectAll(self):
        for widget in self.stack.walk():
            if isinstance(widget, BaseWidget):
                widget.checkbox.active = True

    def SelectNone(self):
        for widget in self.stack.walk():
            if isinstance(widget, BaseWidget):
                widget.checkbox.active = False

    def GetWidgetbyKey(self, key):
        r = None
        for widget in self.stack.walk():
            if isinstance(widget, BaseWidget):
                if widget.FileKey == key:
                    r = widget
        return r

    def GetWidgetsInfos(self):
        res = []
        for widget in self.stack.walk():
            if isinstance(widget, BaseWidget):
                res.append({"checked": widget.ids.checkbox.active, "name": widget.name, "key": widget.FileKey, "imdb id": widget.imdb_id, "tmdb id": widget.tmdb_id})
        return res

    def GetCheckedWidgetsInfos(self):
        res = []
        for widget in self.stack.walk():
            if isinstance(widget, BaseWidget):
                if widget.ids.checkbox.active is True:
                    if not hasattr(widget, 'imdb_id'):
                        imdb = None
                    else:
                        imdb = widget.imdb_id
                    if not hasattr(widget, 'tmdb_id'):
                        tmdb = None
                    else:
                        tmdb = widget.tmdb_id
                    res.append({"name": widget.name, "key": widget.FileKey, "imdb id": imdb, "tmdb id": tmdb})
        return res

    def SetNextPage(self):
        if self.actual_page_number < self.page_numbers-1:
            self.actual_page_number += 1
            self.display_widgets()
        else:
            pass    # TODO : grey the next btn

    def SetPreviousPage(self):
        if self.actual_page_number > 0:
            self.actual_page_number -= 1
            self.display_widgets()
        else:
            pass    # TODO : grey the previous btn

    def SetStyle(self, style):
        self.actualstyle = style
        self.display_widgets()
