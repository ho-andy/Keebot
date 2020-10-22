import random
from asyncio import sleep
from datetime import *

from discord.ext import commands, tasks

import Constants
from YTDLSource import *


class Music(commands.Cog):
    random.seed()

    def __init__(self, bot):
        self.bot = bot
        self.smooth_jazz.start()

    @commands.command(brief='Play random taeha asmr but also breaks like 20s in')
    async def asmr(self, ctx):
        async with ctx.typing():
            asmr_list = Constants.CONST_ASMR_LIST
            url = asmr_list[random.randint(0, len(asmr_list))]
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command(brief='Play youtube video via URL')
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def die(self, ctx):
        """Stops and disconnects the bot from voice"""
        try:
            await ctx.voice_client.disconnect()
        except:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                await ctx.voice_client.disconnect()
                print('Zombie DC')

    @asmr.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.command(brief='Reconnect bot to voice to disconnect zombie bot')
    async def broke_dc(self, ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
            await ctx.voice_client.disconnect()

    @commands.command(brief='In case smooth jazz time fails')
    async def jazz(self, ctx):
        tomfoolery = self.bot.get_channel(Constants.D_CHANNEL_ID)  # specific channel id
        members = tomfoolery.members

        if len(members) > 0:
            for member in members:
                if member.id == Constants.D_MEMBER_ID:  # specific member's id
                    # https://stackoverflow.com/questions/63036753/discord-py-bot-how-to-play-audio-from-local-files
                    voice_client = await tomfoolery.connect()
                    voice_client.play((discord.FFmpegPCMAudio(executable='C:/Program Files/FFmpeg/bin/ffmpeg.exe',
                                                              source=
                                                              Constants.SMOOTH_JAZZ_PATH)))
                    print('playing bob acri')
                    while voice_client.is_playing():
                        await sleep(.1)
                    await voice_client.disconnect()

    @tasks.loop(hours=24)
    async def smooth_jazz(self):
        tomfoolery = self.bot.get_channel(Constants.D_CHANNEL_ID)  #specific channel id
        members = tomfoolery.members

        if len(members) > 0:
            for member in members:
                if member.id == Constants.D_MEMBER_ID:  #specific member's id
                    # https://stackoverflow.com/questions/63036753/discord-py-bot-how-to-play-audio-from-local-files
                    voice_client = await tomfoolery.connect()
                    voice_client.play((discord.FFmpegPCMAudio(executable='C:/Program Files/FFmpeg/bin/ffmpeg.exe',
                                                              source=
                                                              Constants.SMOOTH_JAZZ_PATH)))
                    print('playing bob acri')
                    while voice_client.is_playing():
                        await sleep(.1)
                    await voice_client.disconnect()

    @smooth_jazz.before_loop
    async def before_smooth_jazz(self):
        eleven = 23
        thirty = 30
        await self.bot.wait_until_ready()
        now = datetime.now()
        future = datetime(now.year, now.month, now.day, eleven, thirty)
        if now.hour >= eleven and now.minute >= thirty:
            future += timedelta(days=1)
        await asyncio.sleep((future-now).seconds)
