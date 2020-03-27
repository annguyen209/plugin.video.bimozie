from utils.mozie_request import Request
from xomphimhay.parser.category import Parser as Category
from xomphimhay.parser.channel import Parser as Channel
from xomphimhay.parser.movie import Parser as Movie
import urllib, pickle
import utils.xbmc_helper as helper


class Xomphimhay:
    domain = "https://xomphimhay.com"
    api = "https://xomphimhay.com/api/v1/episodes/%s/player"

    def __init__(self):
        self.request = Request(session=True)
        if helper.has_file_path('xomphimhay.bin'):
            with open(helper.get_file_path('xomphimhay.bin')) as f:
                self.request.set_session(pickle.load(f))

    def updateSession(self):
        with open(helper.get_file_path('xomphimhay.bin'), 'wb') as f:
            pickle.dump(self.request.get_request_session(), f)

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response), Channel().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s/trang-%d/' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = self.request.get(url)
        return Channel().get(response)

    def getMovie(self, url):
        response = self.request.get(url)
        url = Movie().get_movie_link(response)
        response = self.request.get(url)
        self.updateSession()
        return Movie().get(response)

    def getLink(self, movie):
        # https://xemphimso.tv/api/v1/episodes/1000289/player
        response = self.request.get(self.api % movie['link'])
        return Movie().get_link(response, self.domain, self.request)

    def search(self, text, page=1):
        url = "%s/tim-kiem/%s/" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url)
        return Channel().get(response)
