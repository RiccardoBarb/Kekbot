import yaml
import os
import pandas as pd


class Chat:
    def __init__(self, chat_config, twitchio_obj=None):
        """chat_config: is a dictionary specifying the channel names and channel-specific settings
        twitchio_obj: is the twitchio object containing the log of chat events."""

        self.channel_names = [eval(items['name']) for (channel, items) in chat_config.items()]
        self.only_mods = [items['only_mods'] for (channel, items) in chat_config.items()]
        self.twitchio_obj = twitchio_obj
        self.log_columns = ['author_id', 'author_name', 'is_mod', 'is_sub', 'is_turbo', 'message',
                            'channel', 'timestamp']
        self.log_content = []

    @staticmethod
    def load_chat_config(chat_config):
        with open(chat_config) as f:
            chat_config = yaml.load(f, Loader=yaml.FullLoader)
            return chat_config

    def is_highlight(self):
        if 'msg-id' in self.twitchio_obj.tags and \
                self.twitchio_obj.tags['msg-id'] == 'highlighted-message':
            return True
        else:
            return False

    def cache_log(self):
        """we update the log list with basic info on author, channel and message"""
        self.log_content.append(
            [self.twitchio_obj.author.id, self.twitchio_obj.author.name, self.twitchio_obj.author.is_mod,
             self.twitchio_obj.author.is_subscriber, self.twitchio_obj.author.is_turbo, self.twitchio_obj.content,
             self.twitchio_obj.channel.name, self.twitchio_obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')])
        return self

    def to_dataframe(self):
        """logging basic info using pd dataframe"""
        df = pd.DataFrame(self.log_content, columns=self.log_columns)
        return df
