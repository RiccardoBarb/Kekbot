import os
from datetime import datetime
from time import perf_counter
from urllib.parse import urlparse
import urllib.request
import json


class Emote:

    def __init__(self):
        """ The Emote class is used to retrieve the requested emote through BTTV and Twitchemotes API.
         It is initialized with 3 variables:

         reference: an empty string which should either contain a direct url to the emote/image or the corresponding
         Twitch/BTTV command. N.B. it should only contain 1 string (e.g either 'Kappa' or 'KEKW', not both) ;
         identity: a dictionary with the bot token and the client ID. Not used for now but it can be useful to directly
         access Twitch API (for example for getting channel-specific emotes using the corresponding command e.g.'damide1Hi');
         emote_list: an empty dictionary. The methods get_bttv_emotes and get_twitch_emotes fill the dictionary with
         emotes commands as keys and their corresponding ID as values."""

        self.reference = ''
        self.identity = {'token': os.environ['TMI_TOKEN'], 'ID': os.environ['CLIENT_ID']}
        self.emotes_list = {}

    @staticmethod
    def is_url(string):
        reference = urlparse(string)
        if not (reference.scheme and reference.netloc):
            return False
        else:
            return True

    def get_bttv_emotes(self, offset, limit):

        """offset and limit are integers. offset sets the starting emote in the list, limit should be max 100
        (max number of emotes per page)"""

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

    def get_twitch_emotes(self, set_number):

        """set_number needs to be a an integer between 0 and 5 for standard emotes"""

        emotes_list = self.emotes_list
        url = 'https://api.twitchemotes.com/api/v4/channels/' + str(set_number)
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
            sorted_data_list = sorted(data_list, reverse=True)

            with open(sorted_data_list[0]) as json_file:
                self.emotes_list = json.load(json_file)

            print('Data loaded successfully!')

        except (NotADirectoryError, FileNotFoundError):
            print('Data not found\nDownloading new data\n')
            start = perf_counter()
            print('Start download from Twitch and BTTV')
            [self.get_twitch_emotes(i) for i in range(6)]
            [self.get_bttv_emotes(i * 100, 100) for i in range(11)]
            stop = perf_counter()
            print('Done! Elapsed time:' + str(round(stop - start)) + 's')

    def retrieve_emote(self):
        if Emote.is_url(self.reference):
            final_url = self.reference
        else:
            twitch_url_a = 'https://static-cdn.jtvnw.net/emoticons/v2/'
            twitch_url_b = '/default/dark/2.0'
            bttv_url_a = 'https://cdn.betterttv.net/emote/'
            bttv_url_b = '/2x'

            if self.reference in self.emotes_list:
                test_twitch_url = twitch_url_a + str(self.emotes_list[self.reference]) + twitch_url_b
                test_bttv_url = bttv_url_a + str(self.emotes_list[self.reference]) + bttv_url_b
                final_url = 'NotFound'
                try:
                    test = urllib.request.urlopen(test_twitch_url)
                    final_url = test_twitch_url

                except urllib.error.HTTPError:
                    test = urllib.request.urlopen(test_bttv_url)
                    final_url = test_bttv_url

                finally:
                    return final_url
            else:
                final_url = 'UnknownEmote'

        return final_url
