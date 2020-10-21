import os
from datetime import datetime
from time import perf_counter
from urllib.parse import urlparse
import urllib.request
import json


class Emote:

    # The Emote class is used to retrieve the requested emote through BTTV and Twitchemotes API.
    # It is initialized with 3 variables:
    #
    # reference - an empty string which should either contain a direct url to the emote/image or the corresponding
    #   Twitch/BTTV command. N.B. it should only contain 1 string (e.g either 'Kappa' or 'KEKW', not both) ;
    # identity - a dictionary with the bot token and the client ID. Not used for now but it can be useful to directly
    #   access Twitch API (for example for getting channel-specific emotes using the corresponding command e.g.
    #   'damide1Hi');
    # emote_list - an empty dictionary. The methods get_bttv_emotes and get_twitch_emotes fill the dictionary with
    #   emotes commands as keys and their corresponding ID as values.

    def __init__(self):
        self.reference = ''
        self.identity = {'token': os.environ['TMI_TOKEN'], 'ID': os.environ['CLIENT_ID']}
        self.emotes_list = {}

    def has_url(self):
        reference = urlparse(self.reference)
        if not (reference.scheme and reference.netloc):
            return False
        else:
            return True

    def get_bttv_emotes(self, offset, limit):

        emotes_list = self.emotes_list
        url = 'https://api.betterttv.net/3/emotes/shared/top?offset=' + str(offset) + '&limit=' + str(limit)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        url_content = urllib.request.urlopen(req)
        url_data = url_content.read()
        encoding = url_content.info().get_content_charset('utf-8')
        json_content = json.loads(url_data.decode(encoding))

        for i in range(0, len(json_content)):
            emote = json_content[i]['emote']
            code = emote['code']
            if code not in emotes_list:
                ids = emote['id']
                emotes_list[code] = ids

    def get_twitch_emotes(self):

        emotes_list = self.emotes_list
        url = 'https://api.twitchemotes.com/api/v4/channels/0'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        url_content = urllib.request.urlopen(req)
        url_data = url_content.read()
        encoding = url_content.info().get_content_charset('utf-8')
        json_content = json.loads(url_data.decode(encoding))

        for i in range(0, len(json_content['emotes'])):
            emote = json_content['emotes'][i]
            code = emote['code']
            if code not in emotes_list:
                ids = emote['id']
                emotes_list[code] = ids

    def save_emotes(self):
        wd = os.getcwd()
        today = str(datetime.today().date())
        data_dir = wd + '/data'

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        with open(data_dir + '/emote_list_' + today + '.json', 'w') as fp:
            json.dump(self.emotes_list, fp)

        print('saved emote list in' + data_dir)

    def load_recent_emotes(self):
        try:
            wd = os.getcwd()
            data_dir = wd + '/data'

            if not os.path.exists(data_dir):
                raise NotADirectoryError

            elif not any([i for i in os.listdir(data_dir) if i.endswith('.json')]):
                raise FileNotFoundError

            data_list = [data_dir + '/' + i for i in os.listdir(data_dir) if i.endswith('.json')]
            #TODO: why doesn't this work?
            #sorted_data_list = data_list.sort(key=os.path.getctime)

            with open(data_list[0]) as json_file:
                self.emotes_list = json.load(json_file)

            print('Data loaded successfully!')

        except (NotADirectoryError, FileNotFoundError):
            print('Data not found\nDownloading new data\n')
            start = perf_counter()
            print('Start download from Twitch and BTTV')
            self.get_twitch_emotes()
            [self.get_bttv_emotes(i * 100, 100) for i in range(10)]
            stop = perf_counter()
            print('Done! Elapsed time:' + str(round(stop - start)) + 's')
