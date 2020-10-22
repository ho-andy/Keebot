from discord.ext import commands
from datetime import *
from pytz import *


class Timezone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    help_message = """Obtain list of available timezones with '`tz'\n
[timezone] to output timestamp of target timezone\n
[timezone] [hhmm] where hhmm are hours and minutes in 24h notation to apply to target timezone before conversion\n
[timezone] [hhmm] [mmdd] where mmdd are month and day to apply to target timezone before conversion"""

    @commands.command(brief='List available timezones to convert from. `help tz for timezone help',
                      help=help_message)
    async def tz(self, ctx):
        await ctx.send(
            """```'PST': 'Vancouver/Los Angeles'
'MST': 'Edmonton/Denver'
'CST': 'Winnipeg/Dallas/Chicago'
'EST': 'Toronto/New York'
'GMT': 'UTC'
'ICT': 'Vietnam'
'ACT': 'Singapore/China/Perth/Philippines'
'AEST': 'Melbourne/Sydney'```"""
        )

    @commands.command()
    async def pst(self, ctx, *args):
        if len(args) == 0:  # no time specified, print target timezone time
            await ctx.message.delete()
            await ctx.send(await tz_to_est('PST', '', ''))
        elif len(args) == 1:  # standard conversion with time only
            await ctx.message.delete()
            await ctx.send(await tz_to_est('PST', args[0], ''))
        elif len(args) == 2:  # incl date conversion
            await ctx.message.delete()
            await ctx.send(await tz_to_est('PST', args[0], args[1]))

    @commands.command()
    async def mst(self, ctx, *args):
        if len(args) == 0:  # no time specified, print target timezone time
            await ctx.message.delete()
            await ctx.send(await tz_to_est('MST', '', ''))
        elif len(args) == 1:  # standard conversion with time only
            await ctx.message.delete()
            await ctx.send(await tz_to_est('MST', args[0], ''))
        elif len(args) == 2:  # incl date conversion
            await ctx.message.delete()
            await ctx.send(await tz_to_est('MST', args[0], args[1]))

    @commands.command()
    async def cst(self, ctx, *args):
        if len(args) == 0:  # no time specified, print target timezone time
            await ctx.message.delete()
            await ctx.send(await tz_to_est('CST', '', ''))
        elif len(args) == 1:  # standard conversion with time only
            await ctx.message.delete()
            await ctx.send(await tz_to_est('CST', args[0], ''))
        elif len(args) == 2:  # incl date conversion
            await ctx.message.delete()
            await ctx.send(await tz_to_est('CST', args[0], args[1]))

    @commands.command()
    async def est(self, ctx, *args):
        if len(args) == 0:  # no time specified, print target timezone time
            await ctx.message.delete()
            await ctx.send(await tz_to_est('EST', '', ''))
        elif len(args) == 1:  # standard conversion with time only
            await ctx.message.delete()
            await ctx.send(await tz_to_est('EST', args[0], ''))
        elif len(args) == 2:  # incl date conversion
            await ctx.message.delete()
            await ctx.send(await tz_to_est('EST', args[0], args[1]))

    @commands.command()
    async def gmt(self, ctx, *args):
        if len(args) == 0:  # no time specified, print target timezone time
            await ctx.message.delete()
            await ctx.send(await tz_to_est('GMT', '', ''))
        elif len(args) == 1:  # standard conversion with time only
            await ctx.message.delete()
            await ctx.send(await tz_to_est('GMT', args[0], ''))
        elif len(args) == 2:  # incl date conversion
            await ctx.message.delete()
            await ctx.send(await tz_to_est('GMT', args[0], args[1]))

    @commands.command()
    async def ict(self, ctx, *args):
        if len(args) == 0:  # no time specified, print target timezone time
            await ctx.message.delete()
            await ctx.send(await tz_to_est('ICT', '', ''))
        elif len(args) == 1:  # standard conversion with time only
            await ctx.message.delete()
            await ctx.send(await tz_to_est('ICT', args[0], ''))
        elif len(args) == 2:  # incl date conversion
            await ctx.message.delete()
            await ctx.send(await tz_to_est('ICT', args[0], args[1]))

    @commands.command()
    async def act(self, ctx, *args):
        if len(args) == 0:  # no time specified, print target timezone time
            await ctx.message.delete()
            await ctx.send(await tz_to_est('ACT', '', ''))
        elif len(args) == 1:  # standard conversion with time only
            await ctx.message.delete()
            await ctx.send(await tz_to_est('ACT', args[0], ''))
        elif len(args) == 2:  # incl date conversion
            await ctx.message.delete()
            await ctx.send(await tz_to_est('ACT', args[0], args[1]))

    @commands.command()
    async def aest(self, ctx, *args):
        if len(args) == 0:  # no time specified, print target timezone time
            await ctx.message.delete()
            await ctx.send(await tz_to_est('AEST', '', ''))
        elif len(args) == 1:  # standard conversion with time only
            await ctx.message.delete()
            await ctx.send(await tz_to_est('AEST', args[0], ''))
        elif len(args) == 2:  # incl date conversion
            await ctx.message.delete()
            await ctx.send(await tz_to_est('AEST', args[0], args[1]))


# target timezone, user inputted time, user inputted date

async def tz_to_est(from_tz: str, input_time: str, input_date: str):
    """helper function to convert timezones"""

    timezone_dict = {
        'PST': 'America/Vancouver',
        'MST': 'America/Edmonton',
        'CST': 'America/Winnipeg',
        'EST': 'America/Toronto',
        'GMT': 'UTC',
        'ICT': 'Asia/Ho_Chi_Minh',
        'ACT': 'Asia/Singapore',
        'AEST': 'Australia/Sydney'
    }

    output_format = '%I:%M%p %b %d %Z'  # %I: 12h clock - %M: Mins - %p: AM/PM - %b: AbbvMonth - %d: Day - %Z: Timezone

    from_timestamp = datetime.now(timezone(timezone_dict[from_tz]))

    # obtain hour and minute from user input if exists
    if input_time:
        conv_from_time = input_time
        conv_from_hour = int(conv_from_time[0:2])
        conv_from_min = int(conv_from_time[2:4])

        # obtain current timestamp in target timezone with time replaced
        from_timestamp = from_timestamp.replace(hour=conv_from_hour, minute=conv_from_min)

    # obtain month and day from user input if exists
    if input_date:
        conv_from_date = input_date
        conv_from_month = int(conv_from_date[0:2])
        conv_from_day = int(conv_from_date[2:4])

        # obtain current timestamp in target timezone with time replaced
        from_timestamp = from_timestamp.replace(month=conv_from_month, day=conv_from_day)

    # conversion to EST
    to_timestamp = from_timestamp.astimezone(timezone(timezone_dict['EST']))

    return from_timestamp.strftime(output_format) + ' is ' + to_timestamp.strftime(output_format)
