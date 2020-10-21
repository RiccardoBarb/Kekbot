import os
from urllib.parse import urlparse
import urllib.request
import json


class Emote:

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