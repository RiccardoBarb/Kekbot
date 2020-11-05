import os
from twitchio.ext import commands
import kekfunc
import emote
import chat

# GENERAL SETUP
# load channel config and initialize chat object
chat_config = chat.Chat.load_chat_config('utils/config.yaml')
chat_object = chat.Chat(chat_config)
# set up the bot
bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=chat_object.channel_names
)
# initialize emote and load emote list
e = emote.Emote()
e.load_recent_emotes()

# DEFINE COMMANDS
@bot.event
async def event_ready():
    """"" Called once when the bot goes online """
    for i in range(len(chat_object.channel_names)):
        print(f"{os.environ['BOT_NICK']} is connected to {chat_object.channel_names[i]}")


@bot.command(name='kekwho')
async def kekwho(ctx):
    await ctx.send('Hello there :) I am Kekbot. I transform Twitch emotes into shitty braille art. '
                   'Type !kekhow and learn how to use me')


@bot.command(name='kekhow')
async def kekhow(ctx):
    """TODO: add personalized channel messages"""
    await ctx.send('Redeem the reward, then type !kekthis or !kekthat followed by the emote or the emote link.'
                   ' Look here for an example: https://github.com/RiccardoBarb/Kekbot')


@bot.command(name='kekthis')
async def kekthis(ctx):
    """TODO: log requested emotes"""
    chat_object.twitchio_obj = ctx
    channel_id = chat_object.channel_names.index(chat_object.twitchio_obj.channel.name)
    if chat_object.only_mods[channel_id] and chat_object.twitchio_obj.author.is_mod:
        command_and_link = ctx.content
        message_to_chat = kekfunc.handle_request(command_and_link)
        await ctx.send(message_to_chat)
    elif not chat_object.only_mods[channel_id]:
        command_and_link = ctx.content
        message_to_chat = kekfunc.handle_request(command_and_link)
        await ctx.send(message_to_chat)
    else:
        pass


@bot.command(name='kekthat')
async def kekthat(ctx):
    chat_object.twitchio_obj = ctx
    channel_id = chat_object.channel_names.index(chat_object.twitchio_obj.channel.name)
    if chat_object.only_mods[channel_id] and chat_object.twitchio_obj.author.is_mod:
        command_and_link = ctx.content
        message_to_chat = kekfunc.handle_request(command_and_link)
        await ctx.send(message_to_chat)
    elif not chat_object.only_mods[channel_id]:
        command_and_link = ctx.content
        message_to_chat = kekfunc.handle_request(command_and_link)
        await ctx.send(message_to_chat)
    else:
        pass



@bot.command(name='test')
async def test(ctx):
    chat_object.twitchio_obj = ctx
    channel_id = chat_object.channel_names.index(chat_object.twitchio_obj.channel.name)
    if chat_object.only_mods[channel_id] and chat_object.twitchio_obj.author.is_mod:
        await ctx.send('the author is a mod, do something')
    elif not chat_object.only_mods[channel_id]:
        await ctx.send('the author is not a mod, do something anyways')
    else:
        await ctx.send('only mods can do something')

# RUN THE BOT
if __name__ == "__main__":
    bot.run()
