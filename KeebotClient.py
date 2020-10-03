from typing import List
import discord
from discord.ext import commands
from Currency import *
from Music import *
import pickle
import os.path
import random
import sys
import Constants

random.seed()
bot = commands.Bot(command_prefix='`')


@bot.event
async def on_ready():
    print('We have logged in as {}'.format(bot.user))


@bot.command(brief='Hello world!')
async def hellr(ctx):
    await ctx.send("hellrrrrrrrrrr")


@bot.command(brief='View/modify list of sites',
             help="""No arguments to list sites\nadd [site] to add site\ndel/rem [site] to delete site""")
async def site(ctx, *args):  # *args needed to read multiple variables even if unused
    await dict_helper(ctx, siteDict, Constants.SITE_DICT_PATH)


@bot.command(brief='View/modify list of typing sites',
             help="""No arguments to list typing sites\nadd [site] to add typing site
del [site] to delete typing site""",
             name='type')
async def typing(ctx, *args):
    await dict_helper(ctx, typeDict, Constants.TYPE_DICT_PATH)


@bot.command(brief='View and alter tags for sites',
             help="""No arguments to list tags\n[tag,...] to view sites for tag\n[add/rem/del] [tag] to add or remove tag
[tag] [site] to tag site
[tag] [site] [rem/del] to untag site""")
async def tag(ctx, *args):
    arguments = len(ctx.args)
    print(ctx.args)

    if arguments == 1:  # list tags
        send_string = '```\n'
        for alias in tagDict:
            send_string += alias + '\n'
        send_string += '```\n'
        await ctx.send(send_string)
    elif arguments == 2:  # list sites for a particular tag
        if ',' in ctx.args[1]:  # if multiple tags
            input_tag_list = ctx.args[1].split(',')
            send_string = 'Tags: ' + ctx.args[1] + '\n'
            for input_tag in input_tag_list:
                if input_tag.strip() in tagDict:
                    for siteDict_row in tagDict.get(input_tag.strip()):
                        send_string += '|  {}  |  <{}>'.format(siteDict_row, siteDict.get(siteDict_row)) + '\n'
                else:
                    await ctx.send(input_tag + ' does not exist in tag list')
            await ctx.send(send_string)
        else:  # if single tag
            input_tag = ctx.args[1]
            if input_tag in tagDict:
                send_string = 'Tag: ' + input_tag + '\n'
                for siteDict_row in tagDict.get(input_tag):
                    send_string += '|  {}  |  <{}>'.format(siteDict_row, siteDict.get(siteDict_row)) + '\n'
                await ctx.send(send_string)
            else:
                await ctx.send(input_tag + ' does not exist in tag list')
    elif arguments == 3:  # add site to a particular tag
        input_tag = str(ctx.args[1])
        input_site = str(ctx.args[2])

        if input_tag == 'rem' or input_tag == 'del' or input_tag == 'rm':  # if input is removal instead of tag
            if input_site in tagDict:  # input_site is the tag to add/remove in this scope
                tagDict.pop(input_site)
                await ctx.send('Removed ' + input_site + ' tag')
            else:
                await ctx.send(input_site + ' does not exist for removal')
        elif input_tag == 'add':  # if input is adding instead of tag
            if input_site not in tagDict:  # input_site is the tag to add/remove in this scope
                tagDict[input_site] = []
                await ctx.send('Added ' + input_site + ' tag')
            else:
                await ctx.send(input_site + ' already exists as a tag')
        elif input_tag in tagDict and input_site in siteDict:  # if input_tag is neither an add or remove
            tagDict[input_tag].append(input_site)
            await ctx.send(input_site + ' added to ' + input_tag + ' tag')
        else:
            await ctx.send('Either tag or site does not exist or not add/rem/del/rm command')
    elif arguments == 4:  # remove site from a particular tag
        input_tag = str(ctx.args[1])
        input_site = str(ctx.args[2])
        rem_command = str(ctx.args[3])

        if rem_command == 'rem' or rem_command == 'del':
            if input_tag in tagDict and input_site in tagDict[input_tag]:
                tagDict[input_tag].remove(input_site)
                await ctx.send('Removed ' + input_site + ' from ' + input_tag)
            else:
                await ctx.send('Tag or site does not exist')
        else:
            await ctx.send("To untag a site, use 'rem' or 'del' as the 3rd argument")
    else:
        await ctx.send('Too many arguments')

    pickle.dump(tagDict, open(Constants.TAG_DICT_PATH, 'wb'))


@bot.command(brief='View and alter shopping list',
             help='')
async def shop(ctx, *args):
    if len(ctx.args) > 1:
        if ctx.args[1] == 'share':  # to show combined list
            send_string = ''
            for item in sorted({**aDict, **bDict}):
                send_string += '|  {}  |  <{}>'.format(item, {**aDict, **bDict}.get(item)) + '\n'
            await ctx.send(send_string)
            return

    author = str(ctx.message.author)
    pickle_file = (Constants.KEEBOT_PATH + author + 'ShopDict.p')
    if author == 'Doom#4859':
        await dict_helper(ctx, aDict, pickle_file)
    elif author == '『𝕤𝕪𝕟』#5873':
        await dict_helper(ctx, bDict, pickle_file)
    else:
        await ctx.send(author + ' does not exist')


def load_dict(pickle_file: str) -> dict:
    loaded_dict = {}
    if os.path.exists(pickle_file):
        loaded_dict = pickle.load((open(pickle_file, 'rb')))
    return loaded_dict


def load_list(pickle_file: str) -> List:
    loaded_list = []
    if os.path.exists(pickle_file):
        loaded_list = pickle.load((open(pickle_file, 'rb')))
    return loaded_list


async def list_helper(ctx, item_list: List, pickle_file: str):  # method for list commands with view/add/remove
    arguments = len(ctx.args)
    print(ctx.args)

    if arguments == 1:  # view list
        await ctx.send('<{}>'.format('>\n<'.join(item_list)))
    elif arguments == 2:
        await ctx.send('More arguments required')
    elif arguments == 3:  # add or remove item
        if ctx.args[1] == 'add':
            if ctx.args[2] in item_list:
                await ctx.send(ctx.args[2] + ' already exists')
            else:
                item_list.append(ctx.args[2])
                item_list.sort()
                await ctx.send('Added <' + ctx.args[2] + '>')
        elif ctx.args[1] == 'del' or ctx.args[1] == 'rem':
            if ctx.args[2] not in item_list:
                await ctx.send(ctx.args[2] + ' does not exist')
            else:
                item_list.remove(ctx.args[2])
                item_list.sort()
                await ctx.send('Removed <' + ctx.args[2] + '>')
        else:
            await ctx.send('Command not recognised')
    else:
        await ctx.send('Too many arguments')

    pickle.dump(item_list, open(pickle_file, 'wb'))


async def dict_helper(ctx, item_dict: dict, pickle_file: str):  # method for dict commands with view/add/remove
    arguments = len(ctx.args)
    print(ctx.args)
    print(item_dict)

    if arguments == 1:  # view list
        send_string = ''
        for item in sorted(item_dict):
            if len(send_string) + len(item) > 1900:  # 2000 character limit per message
                await ctx.send(send_string)
                send_string = '|  {}  |  <{}>'.format(item, item_dict.get(item)) + '\n'
            else:
                send_string += '|  {}  |  <{}>'.format(item, item_dict.get(item)) + '\n'
        await ctx.send(send_string)
    elif arguments == 2:  # view link for entered alias
        alias = ctx.args[1]
        if alias in item_dict:
            await ctx.send('|  {}  |  <{}>'.format(alias, item_dict.get(alias)))
        else:
            await ctx.send(alias + ' does not exist')
    elif arguments == 3 or arguments == 4:  # add or remove from dict
        command = ctx.args[1]  # add, rem
        alias = ctx.args[2]  # alias of link
        if command == 'add':
            link = ctx.args[3]  # actual link
            if alias in item_dict:
                await ctx.send(alias + ' already exists')
            else:
                item_dict[alias] = link
                await ctx.send('Added <' + alias + '>')
        elif command == 'del' or command == 'rem' or command == 'rm':
            if alias not in item_dict:
                await ctx.send(alias + ' does not exist')
            else:
                item_dict.pop(alias)
                await ctx.send('Removed <' + alias + '>')
        else:
            await ctx.send('Command not recognised')
    else:
        await ctx.send('Too many arguments')

    pickle.dump(item_dict, open(pickle_file, 'wb'))


@bot.command()
async def kms(ctx):
    await ctx.message.delete()
    await bot.close()
    sys.exit()

# for if need to initialise any dicts. comment out load_dict below if so
siteDict = {'1up': 'https://1upkeyboards.com/',
'apex': 'https://apexkeyboards.ca/',
'ash': 'https://ashkeebs.com/?v=3e8d115eb4b3/',
'aura': 'https://auramech.com/',
'candy': 'https://candykeys.com/',
'via': 'https://caniusevia.com/',
'cannon': 'https://cannonkeys.com/',
'dclack': 'https://dailyclack.com/',
'deskeys': 'https://deskeys.io/',
'deskhero': 'https://deskhero.ca/',
'dixie': 'https://dixiemech.store/',
'wei': 'https://kbdfans.com/',
'kebo': 'https://kebo.store/',
'kalendar': 'https://keycaplendar.firebaseapp.com/',
'kyle': 'https://keyforge.com/',
'kofi': 'https://keyspresso.ca/',
'kiiboss': 'https://kiiboss.studio/',
'kono': 'https://kono.store/',
'kpr': 'https://kprepublic.com/',
'max': 'https://maxkeyboard.com/',
'mk': 'https://mechanicalkeyboards.com/shop/',
'nk': 'https://novelkeys.xyz/',
'origin': 'https://originativeco.com/',
'space': 'https://spacecables.net/',
'krelbit': 'https://switchmod.net/',
'tkc': 'https://thekey.company/',
'ai03': 'https://ai03.me/',
'prime': 'https://primekb.com/',
'goat': 'https://theremingoat.com/',
'tx': 'https://us.txkeyboards.com/',
'zeal': 'https://zealpc.net/',
'wooting': 'https://wooting.io/'}
typeDict = {'monkey': 'https://monkey-type.com/',
            'cat': 'https://thetypingcat.com/',
            '10': 'https://10fastfingers.com/typing-test/english',
            'academy': 'https://typing.academy/typing-tutor/lessons',
            'ya': 'https://yatyper.com/',
            'keybr': 'https://keybr.com/',
            'gg': 'https://typings.gg/',
            'io': 'https://typetest.io/'}
tagDict = {
    'switches': ['1up', 'apex', 'aura', 'candy', 'dclack', 'kebo', 'kono', 'mk', 'mkultra', 'nk', 'prime', 'tkc', 'wei', 'switches'],
    'stabs': ['1up', 'apex', 'aura', 'cannon', 'dclack', 'kebo', 'kofi', 'kpr', 'zeal'],
    'kits': ['1up', 'cannon', 'deskeys', 'dixie', 'kebo', 'kpr', 'nk', 'origin', 'tkc', 'tx', 'wei', 'zeal'],
    'lube': ['apex', 'ash', 'dclack', 'krelbit', 'tx', 'zeal'],
    'keycaps': ['1up', 'kpr', 'max', 'mk', 'mkultra', 'prime'],
    'prebuilts': ['candy', 'deskhero', 'kono', 'kpr', 'max', 'mk', 'wooting'],
    'tools': ['1up', 'apex', 'aura', 'dclack', 'kiiboss', 'kofi', 'kpr', 'mk', 'nk', 'prime'],
    'topre': ['1up', 'deskeys'],
    'info': ['ai03', 'goat', 'kalendar'],
    'films': ['apex', 'ash', 'kebo', 'tx'],
    'firmware': ['qmkgui', 'via'],
    'services': ['ash'],
    'artisans': ['alpha', 'jelly', 'kpr', 'kyle', 'mk', 'scraft', 'space', 'summit'],
    'ergo': ['aura', 'mkultra', 'wooting'],
    'springs': ['prime', 'tx'],
    'deskmats': ['aura', 'cannon', 'deskhero', 'kono', 'kpr', 'nk', 'prime', 'tkc', 'tx'],
    'groupbuy': ['candy', 'cannon', 'dclack', 'deskhero', 'dixie', 'kono', 'krelbit', 'nk', 'origin', 'tkc', 'tx', 'wei'],
    'cad': ['apex', 'ash', 'aura', 'deskhero', 'kofi', 'zeal']
}

# load pickles
tagDict = load_dict(Constants.TAG_DICT_PATH)
siteDict = load_dict(Constants.SITE_DICT_PATH)
typeDict = load_dict(Constants.TYPE_DICT_PATH)
bDict = load_dict(Constants.B_DICT_PATH)
aDict = load_dict(Constants.A_DICT_PATH)
shareDict = load_dict(Constants.SHARE_DICT_PATH)

# startup
bot.add_cog(Music(bot))
bot.add_cog(Currency(bot))
bot.run(Constants.DISCORD_SECRET)


