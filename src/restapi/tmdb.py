#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.network.urlrequest import UrlRequest
from kivy.app import App
import datetime
from misc.utils import HTTPToSTR, STRToHTTP
from widgets.thumbnail import ThumbnailWidget
from modal.moviepicker import MoviePicker
from misc.utils import StrFindBetween
from os.path import join
from kivy.logger import Logger
from threads import threadworker


def ThumbnailWidget_on_touch_down(instance, touch):
    if instance.collide_point(*touch.pos):
        instance.app.FieldsStackScreen.TMDB1.Search_TMDB_ID(instance.restid, instance.app.FieldsStackScreen.TMDB1.Search_TMDB_ID_Callback)
        instance.parent_widget.on_close()


class TMDB():
    APIkey = '3b608fc11821e92cd2459320206a9d9b'

    def __init__(self, **kwargs):
        self.app = App.get_running_app()
        self.lang = self.app.Languages[self.app.lang]["tmdb"]

    def Search_Images(self, tmdb_id):
        url = 'https://api.themoviedb.org/3/movie/' + tmdb_id + '/images?api_key=' + self.APIkey + self.lang
        UrlRequest(url, self.Search_Images_Callback)

    def Search_Images_Callback(self, req, res):
        if 'posters' in res:
            view = MoviePicker(auto_dismiss=False)
            view.ids.title.text = 'Posters from TheMovieDB'
            for i in res['posters']:
                posterpath = 'https://image.tmdb.org/t/p/w500' + HTTPToSTR(i['file_path']) + '?api_key=' + self.APIkey + self.lang
                size = '('+str(i['width'])+'X'+str(i['height'])+')'
                Movie = ThumbnailWidget(view, None, size, posterpath)
                view.ids.stack.add_widget(Movie)
                # TODO Bind the on_mouse_down
            view.open()

    def Search_Images_TW_Callback(self, req, res):
        resc = []
        if 'posters' in res:
            for i in res['posters']:
                tab = {}
                tab['source'] = 'https://image.tmdb.org/t/p/w500' + HTTPToSTR(i['file_path']) + '?api_key=' + self.APIkey + self.lang
                tab['text'] = '('+str(i['width'])+'X'+str(i['height'])+')'
                resc.append(tab)
        return resc

    def Search_Movies_Name(self, name):

        url = 'http://api.themoviedb.org/3/search/movie?api_key=' + self.APIkey + '&query=' + STRToHTTP(name) + self.lang
        UrlRequest(url, self.Search_Movies_Name_Callback)

    def Search_Movies_Name_Callback(self, req, res):
        if 'total_results' in res:
            total_results = int(HTTPToSTR(res['total_results']))

            if total_results > 0:
                view = MoviePicker(auto_dismiss=False)

                for i in range(min(total_results, 20)):        # maximum result per page is 20
                    if res['results'][i]['poster_path'] is not None:
                        posterpath = 'https://image.tmdb.org/t/p/w500' + HTTPToSTR(res['results'][i]['poster_path']) + '?api_key=' + self.APIkey + self.lang
                    else:
                        posterpath = join(self.app.root_dir + "/textures/", "none.png")
                    Movie = ThumbnailWidget(view, HTTPToSTR(res['results'][i]['id']), HTTPToSTR(res['results'][i]['title']), posterpath)
                    view.ids.stack.add_widget(Movie)
                    Movie.bind(on_touch_down=ThumbnailWidget_on_touch_down)
                view.open()

    def Search_IMDB_ID(self, imdb_id, callback):
        url = 'http://api.themoviedb.org/3/find/' + imdb_id + '?api_key=' + self.APIkey + '&external_source=imdb_id' + self.lang
        UrlRequest(url, callback)

    def Search_IMDB_ID_Callback(self, req, res):
        resdict = {}
        if 'movie_results' in res:
            if len(res['movie_results']) >= 1:
                if 'overview' in res['movie_results'][0]:
                    resdict['Description'] = HTTPToSTR(res['movie_results'][0]['overview'])
                if 'release_date' in res['movie_results'][0]:
                    resdict['Date'] = datetime.datetime.strptime(HTTPToSTR(res['movie_results'][0]['release_date']), "%Y-%m-%d").strftime(self.app.DateFormat)
                if 'poster_path' in res['movie_results'][0]:
                    resdict['cover_art'] = 'https://image.tmdb.org/t/p/w500' + HTTPToSTR(res['movie_results'][0]['poster_path']) + '?api_key=' + self.APIkey + self.lang
                if 'id' in res['movie_results'][0]:
                    resdict['TMDB id'] = HTTPToSTR(res['movie_results'][0]['id'])
                    self.Search_TMDB_ID(resdict['TMDB id'], self.Search_TMDB_ID_Callback)

        self.app.FieldsStackWidget.Display_res(resdict)

    def Search_IMDB_ID_MASS_Callback(self, req, res):
        resdict = {}

        imdbid = StrFindBetween(req.url, "find/", "?api_key")
        if 'movie_results' in res:
            if len(res['movie_results']) >= 1:
                if 'overview' in res['movie_results'][0]:
                    resdict['Description'] = HTTPToSTR(res['movie_results'][0]['overview'])
                if 'release_date' in res['movie_results'][0]:
                    resdict['Date'] = datetime.datetime.strptime(HTTPToSTR(res['movie_results'][0]['release_date']), "%Y-%m-%d").strftime(self.app.DateFormat)
                if 'poster_path' in res['movie_results'][0]:
                    resdict['cover_art'] = 'https://image.tmdb.org/t/p/w500' + HTTPToSTR(res['movie_results'][0]['poster_path']) + '?api_key=' + self.APIkey + self.lang
                if 'id' in res['movie_results'][0]:
                    resdict['TMDB id'] = HTTPToSTR(res['movie_results'][0]['id'])
                    self.app.FilesStackScreen.MassScrapView.MassScrapThread1.SetTMDB_IDbyIMDB_ID(imdbid, resdict['TMDB id'])
                    self.Search_TMDB_ID(resdict['TMDB id'], self.Search_TMDB_ID_MASS_Callback)

    def Search_TMDB_ID(self, tmdb_id, callback):
        url = 'https://api.themoviedb.org/3/movie/' + tmdb_id + '?api_key=' + self.APIkey + self.lang
        Logger.debug('urlresq:' + url)
        UrlRequest(url, on_success=callback, on_error=self.callbackerr, on_failure=self.callbackerr)

    def callbackerr(self, req, res):
        Logger.debug(res)

    def Search_TMDB_ID_MASS_Callback(self, req, res):
        resdict = {}
        if 'overview' in res:
            resdict['Description'] = HTTPToSTR(res['overview'])

        if 'poster_path' in res:
            resdict['cover_art'] = 'https://image.tmdb.org/t/p/w500' + HTTPToSTR(res['poster_path']) + '?api_key=' + self.APIkey + self.lang

        if 'production_countries' in res:
            if len(res['production_countries']) >= 1:
                countries = []
                for val in res['production_countries']:
                    countries.append(HTTPToSTR(val['iso_3166_1']))
                resdict['Country'] = "\n".join(map(str, countries))

        if 'genres' in res:
            if len(res['genres']) >= 1:
                countries = []
                for val in res['genres']:
                    countries.append(HTTPToSTR(val['name']))
                resdict['Genre'] = "\n".join(map(str, countries))

        if 'title' in res:
            resdict['Name'] = HTTPToSTR(res['title'])

        if 'imdb_id' in res:
            resdict['IMDb ID'] = HTTPToSTR(res['imdb_id'])

        if 'production_companies' in res:
            if len(res['production_companies']) >= 1:
                production_companies = []
                for val in res['production_companies']:
                    production_companies.append(val['name'])
                resdict['Production Company'] = "\n".join(map(str, production_companies))

        if 'release_date' in res:
            if res['release_date'] != '':
                resdict['Date'] = datetime.datetime.strptime(HTTPToSTR(res['release_date']), "%Y-%m-%d").strftime(self.app.DateFormat)

        if 'original_title' in res:
            resdict['Original Title'] = HTTPToSTR(res['original_title'])

        if 'budget' in res:
            resdict['Budget'] = HTTPToSTR(res['budget'])

        if 'id' in res:
            resdict['TMDB id'] = HTTPToSTR(res['id'])

        for field, value in resdict.items():
            if value is not None:
                self.app.MCWS.SetInfo(self.app.FilesStackScreen.MassScrapView.MassScrapThread1.GetFileKeybyTMDB_ID(resdict['TMDB id']), field, value, None)

        if str(self.app.CoverArtMassScrap) == "1":
            self.app.MCWS.SetImage(self.app.FilesStackScreen.MassScrapView.MassScrapThread1.GetFileKeybyTMDB_ID(resdict['TMDB id']), resdict['cover_art'])
            tmb = self.app.FilesStackWidget.GetWidgetbyKey(self.app.FilesStackScreen.MassScrapView.MassScrapThread1.GetFileKeybyTMDB_ID(resdict['TMDB id']))
            tmb.SetImage(resdict['cover_art'])
            tmb.SetText(resdict['Name'])
        self.app.FilesStackScreen.MassScrapView.MassScrapThread1.GetIndex()

    def Search_TMDB_ID_Callback(self, req, res):
        resdict = {}
        if 'overview' in res:
            resdict['Description'] = HTTPToSTR(res['overview'])

        if 'poster_path' in res:
            resdict['cover_art'] = 'https://image.tmdb.org/t/p/w500' + HTTPToSTR(res['poster_path']) + '?api_key=' + self.APIkey + self.lang

        if 'production_countries' in res:
            if len(res['production_countries']) >= 1:
                countries = []
                for val in res['production_countries']:
                    countries.append(HTTPToSTR(val['iso_3166_1']))
                resdict['Country'] = "\n".join(map(str, countries))

        if 'genres' in res:
            if len(res['genres']) >= 1:
                countries = []
                for val in res['genres']:
                    countries.append(HTTPToSTR(val['name']))
                resdict['Genre'] = "\n".join(map(str, countries))

        if 'title' in res:
            resdict['Name'] = HTTPToSTR(res['title'])

        if 'imdb_id' in res:
            resdict['IMDb ID'] = HTTPToSTR(res['imdb_id'])

        if 'production_companies' in res:
            if len(res['production_companies']) >= 1:
                production_companies = []
                for val in res['production_companies']:
                    production_companies.append(HTTPToSTR(val['name']))
                resdict['Production Company'] = "\n".join(map(str, production_companies))

        if 'release_date' in res:
            if res['release_date'] != '':
                resdict['Date'] = datetime.datetime.strptime(HTTPToSTR(res['release_date']), "%Y-%m-%d").strftime(self.app.DateFormat)

        if 'original_title' in res:
            resdict['Original Title'] = HTTPToSTR(res['original_title'])

        if 'budget' in res:
            resdict['Budget'] = HTTPToSTR(res['budget'])

        if 'id' in res:
            resdict['TMDB id'] = HTTPToSTR(res['id'])

        self.app.FieldsStackWidget.Display_res(resdict)
        self.Search_Keywords(resdict['TMDB id'])
        self.Search_Credits(resdict['TMDB id'])
        self.Search_Videos(resdict['TMDB id'])


    def Search_Credits(self, tmdb_id):
        url = 'http://api.themoviedb.org/3/movie/' + tmdb_id + '/credits?api_key=' + self.APIkey + self.lang
        UrlRequest(url, self.Search_Credits_Callback)

    def Search_Credits_Callback(self, req, res):
        resdict = {}
        if 'cast' in res:
            if len(res['cast']) >= 1:
                cast = []
                for val in res['cast']:
                    cast.append(HTTPToSTR(val['name']))
                resdict['Actors'] = "\n".join(map(str, cast))

        if 'crew' in res:
            if len(res['crew']) >= 1:
                Director = []
                Screenplay = []
                Producer = []
                OriginalMusicComposer = []
                ArtDirection = []
                CostumeDesign = []
                MakeupArtist = []
                SoundDesigner = []
                MusicEditor = []
                ExecutiveProducer = []
                DirectorofPhotography = []
                Novel = []
                ProductionDesign = []
                Editor = []
                SoundEditor = []
                for val in res['crew']:
                    if val['job'] == 'Director':
                        Director.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Screenplay':
                        Screenplay.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Producer':
                        Producer.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Executive Producer':
                        ExecutiveProducer.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Director of Photography':
                        DirectorofPhotography .append(HTTPToSTR(val['name']))
                    if val['job'] == 'Editor':
                        Editor.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Art Direction':
                        ArtDirection.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Novel':
                        Novel.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Costume Design':
                        CostumeDesign.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Makeup Artist':
                        MakeupArtist.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Sound Designer':
                        SoundDesigner.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Sound Editor':
                        SoundEditor.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Music Editor':
                        MusicEditor.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Original Music Composer':
                        OriginalMusicComposer.append(HTTPToSTR(val['name']))
                    if val['job'] == 'Production Design':
                        ProductionDesign.append(HTTPToSTR(val['name']))

                # Return a dictionnary with the correct MC key/value Fields

                resdict['Director'] = HTTPToSTR("\n".join(map(str, Director)))
                resdict['Screenwriter'] = HTTPToSTR("\n".join(map(str, Screenplay)))
                resdict['Producer'] = HTTPToSTR("\n".join(map(str, Producer)))
                resdict['Executive Producer'] = HTTPToSTR("\n".join(map(str, ExecutiveProducer)))
                resdict['Cinematographer'] = HTTPToSTR("\n".join(map(str, DirectorofPhotography)))
                resdict['Music By'] = HTTPToSTR("\n".join(map(str, OriginalMusicComposer)))
                resdict['Novel'] = HTTPToSTR("\n".join(map(str, Novel)))
                resdict['Production Design'] = HTTPToSTR("\n".join(map(str, ProductionDesign)))

        self.app.FieldsStackWidget.Display_res(resdict)

    def Search_Keywords(self, tmdb_id):
        url = 'http://api.themoviedb.org/3/movie/' + tmdb_id + '/keywords?api_key=' + self.APIkey + self.lang
        UrlRequest(url, self.Search_Keywords_Callback)

    def Search_Keywords_Callback(self, req, res):
        resdict = {}
        if 'keywords' in res:
            if len(res['keywords']) >= 1:
                keywords = []
                for val in res['keywords']:
                    keywords.append(HTTPToSTR(val['name']))
                resdict['Keywords'] = "\n".join(map(str, keywords))
                self.app.FieldsStackWidget.Display_res(resdict)

    def Search_Videos(self, tmdb_id):
        url = 'http://api.themoviedb.org/3/movie/' + tmdb_id + '/videos?api_key=' + self.APIkey + self.lang
        UrlRequest(url, self.Search_Videos_Callback)

    def Search_Videos2(self, tmdb_id):
        url = 'http://api.themoviedb.org/3/movie/' + tmdb_id + '/videos?api_key=' + self.APIkey
        UrlRequest(url, self.Search_Videos2_Callback)

    def Search_Videos_Callback(self, req, res):
        resdict = {}
        if "results" in res:
            if len(res["results"]) > 0:
                if 'key' in res["results"][0]:
                    resdict['Trailer'] = "https://www.youtube.com/watch?v=" + res["results"][0]["key"]
                    self.app.FieldsStackWidget.Display_res(resdict)
            else:
                tmdbid = StrFindBetween(req.url, "movie/", "/videos")
                self.Search_Videos2(tmdbid)

    def Search_Videos2_Callback(self, req, res):
        resdict = {}
        if "results" in res:
            if len(res["results"]) > 0:
                if 'key' in res["results"][0]:
                    resdict['Trailer'] = "https://www.youtube.com/watch?v=" + res["results"][0]["key"]
                    self.app.FieldsStackWidget.Display_res(resdict)
