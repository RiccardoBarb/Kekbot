import os
from twitchio.ext import commands
import asyncio
import kekfunc
import emote
import chat
from datetime import datetime
import csv
import pasta
import numpy as np

# GENERAL SETUP
# load channel config and initialize chat object
chat_config = chat.Chat.load_chat_config('utils/config.yaml')
chat_object = chat.Chat(chat_config)
# load pasta list
pasta_list, pasta_id = pasta.load_pasta('Data/copypasta/extended_fake_pastas.csv')


# set up the bot
class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            irc_token=os.environ['TMI_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=os.environ['BOT_NICK'],
            prefix=os.environ['BOT_PREFIX'],
            initial_channels=chat_object.channel_names)
        # initialize emote and load emote list
        self.emotes = emote.Emote()
        self.emotes.load_recent_emotes()
        self.pasta_list = pasta_list
        self.pasta_id = pasta_id

    # DEFINE CYCLIC TASKS
    async def dump_cache(self):
        while True:
            await asyncio.sleep(120)
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df = chat_object.dump_to_csv()
            print('dumping cache', now)

    # DEFINE EVENTS
    async def event_ready(self):
        """"" Called once when the bot goes online """
        if chat_object.dump_log:
            asyncio.create_task(self.dump_cache())
            print('logging')
        else:
            print('not logging')

        for i in range(len(chat_object.channel_names)):
            print(f"{os.environ['BOT_NICK']} is connected to {chat_object.channel_names[i]}")

    async def event_message(self, message):
        try:
            channel_id = chat_object.channel_names.index(message.channel.name)
            # channel specific cached logs
            if chat_object.log_chat[channel_id]:
                chat_object.twitchio_obj = message
                chat_object.cache_log()
                print(chat_object.log_content[-1])
                await self.handle_commands(message)

            if 'custom-reward-id' in message.tags:

                if message.tags['custom-reward-id'] == chat_object.kekthis_reward[channel_id]:
                    message_to_chat = kekfunc.handle_request(message.content, self.emotes)
                    await message.channel.send(message_to_chat)
            else:
                await self.handle_commands(message)

        except TypeError:
            await self.handle_commands(message)

    # DEFINE COMMANDS
    @commands.command(name='kekwho')
    async def kekwho(self, ctx):
        await ctx.send('Hello there :) I am Kekbot. I transform Twitch emotes into shitty braille art. '
                       'Type !kekhow and learn how to use me')

    @commands.command(name='kekhow')
    async def kekhow(self, ctx):
        chat_object.twitchio_obj = ctx
        channel_id = chat_object.channel_names.index(chat_object.twitchio_obj.channel.name)
        message = chat_object.kekhow_message[channel_id]
        await ctx.send(message)

    @commands.command(name='kekthis')
    async def kekthis(self, ctx):
        """TODO: log requested emotes"""
        chat_object.twitchio_obj = ctx
        channel_id = chat_object.channel_names.index(chat_object.twitchio_obj.channel.name)
        if chat_object.only_mods[channel_id] and chat_object.twitchio_obj.author.is_mod:
            command_and_link = ctx.content
            message_to_chat = kekfunc.handle_request(command_and_link, self.emotes)
            await ctx.send(message_to_chat)
        elif not chat_object.only_mods[channel_id]:
            command_and_link = ctx.content
            message_to_chat = kekfunc.handle_request(command_and_link, self.emotes)
            await ctx.send(message_to_chat)
        else:
            pass

    @commands.command(name='kekthat')
    async def kekthat(self, ctx):
        chat_object.twitchio_obj = ctx
        channel_id = chat_object.channel_names.index(chat_object.twitchio_obj.channel.name)
        if chat_object.only_mods[channel_id] and chat_object.twitchio_obj.author.is_mod:
            command_and_link = ctx.content
            message_to_chat = kekfunc.handle_request(command_and_link, self.emotes)
            await ctx.send(message_to_chat)
        elif not chat_object.only_mods[channel_id]:
            command_and_link = ctx.content
            message_to_chat = kekfunc.handle_request(command_and_link, self.emotes)
            await ctx.send(message_to_chat)
        else:
            pass

    @commands.command(name='test')
    async def test(self, ctx):
        chat_object.twitchio_obj = ctx
        chat_object.to_dataframe()
        channel_id = chat_object.channel_names.index(chat_object.twitchio_obj.channel.name)
        if chat_object.only_mods[channel_id] and chat_object.twitchio_obj.author.is_mod:
            await ctx.send('the author is a mod, do something')
        elif not chat_object.only_mods[channel_id]:
            await ctx.send('the author is not a mod, do something anyways')
        else:
            await ctx.send('only mods can do something')

    @commands.command(name='kekpasta')
    async def kekpasta(self, ctx):
        chat_object.twitchio_obj = ctx
        channel_id = chat_object.channel_names.index(chat_object.twitchio_obj.channel.name)
        chosen_pasta, self.pasta_list, self.pasta_id = pasta.chose_pasta(self.pasta_list, self.pasta_id)
        if chat_object.only_mods[channel_id] and chat_object.twitchio_obj.author.is_mod:
            print(str(len(self.pasta_list))+' remaining pastas')
            await ctx.send(chosen_pasta)
        elif not chat_object.only_mods[channel_id]:
            print(str(len(self.pasta_list)) + ' remaining pastas')
            await ctx.send(chosen_pasta)
        else:
            print(str(len(self.pasta_list)) + ' remaining pastas')
            await ctx.send(chosen_pasta)


# RUN THE BOT

bot = Bot()
bot.run()
