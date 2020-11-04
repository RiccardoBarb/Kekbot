import yaml
import os


class Chat:
    def __init__(self, chat_config, twitchio_obj=None):
        """chat_config: is a dictionary specifying the channel names and channel-specific settings
        twitchio_obj: is the twitchio object containing the log of chat events."""

        self.channel_names = [eval(items['name']) for (channel, items) in chat_config.items()]
        self.only_mods = [items['only_mods'] for (channel, items) in chat_config.items()]
        self.twitchio_obj = twitchio_obj

    @staticmethod
    def load_chat_config(chat_config):
        with open(chat_config) as f:
            chat_config = yaml.load(f, Loader=yaml.FullLoader)
            return chat_config

    def is_highlight(self):
        if 'msg-id' in self.twitchio_obj.message.tags and \
                self.twitchio_obj.message.tags['msg-id'] == 'highlighted-message':
            return True
        else:
            return False
