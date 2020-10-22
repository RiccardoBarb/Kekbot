import os
from twitchio.ext import commands
import kekfunc
import emote

# set up the bot
bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

is_test = True
# initialize emote and load emote list
e = emote.Emote()
e.load_recent_emotes()

@bot.event
async def event_ready():
    # Called once when the bot goes online'
    print(f"{os.environ['BOT_NICK']} is online!")


@bot.command(name='kekwho')
async def test(ctx):
    await ctx.send('Hello there :) I am Kekbot. I transform Twitch emotes into shitty braille art. '
                   'Type !kekhow and learn how to use me')


@bot.command(name='kekhow')
async def test(ctx):
    await ctx.send('Redeem the reward, then type !kekthis or !kekthat followed by the emote or the emote link.'
                   ' Look here for an example: https://github.com/RiccardoBarb/Kekbot')


@bot.command(name='kekthis')
async def kekthis(ctx):
    if is_test:
        command_and_link = ctx.content
        message_to_chat = kekfunc.handle_request(command_and_link)
        await ctx.send(message_to_chat)
    else:
        if 'msg-id' in ctx.message.tags and ctx.message.tags['msg-id'] == 'highlighted-message':
            command_and_link = ctx.content
            message_to_chat = kekfunc.handle_request(command_and_link)
            await ctx.send(message_to_chat)
        else:
            pass


@bot.command(name='kekthat')
async def kekthat(ctx):
    if is_test:
        command_and_link = ctx.content
        message_to_chat = kekfunc.handle_request(command_and_link)
        await ctx.send(message_to_chat)
    else:
        if 'msg-id' in ctx.message.tags and ctx.message.tags['msg-id'] == 'highlighted-message':
            command_and_link = ctx.content
            message_to_chat = kekfunc.handle_request(command_and_link)
            await ctx.send(message_to_chat)
        else:
            pass


@bot.command(name='test')
async def test(ctx):
    if 'msg-id' in ctx.message.tags and ctx.message.tags['msg-id'] == 'highlighted-message':
        await ctx.send('the message is highlighted')
    else:
        pass


if __name__ == "__main__":
    bot.run()
