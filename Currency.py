from discord.ext import commands
from forex_python.converter import CurrencyRates

currencyRates = CurrencyRates()


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Converts base currency to destination currency')
    async def conv(self, ctx, num: float, base: str, dest: str):
        converted = await convert_curr(num, base, dest)
        await ctx.send(str(num) + ' ' + base.upper() + ' is {:.2f} '.format(converted) + dest.upper())
        await ctx.message.delete()

    @commands.command(brief='Converts USD to CAD')
    async def usd(self, ctx, num: float):
        converted = await convert_usd(num)
        await ctx.send('$' + str(num) + ' USD is {:.2f} CAD'.format(converted))
        await ctx.message.delete()

    @commands.command(brief='Converts EUR to CAD')
    async def eur(self, ctx, num: float):
        converted = await convert_eur(num)
        await ctx.send('€' + str(num) + ' EUR is {:.2f} CAD'.format(converted))
        await ctx.message.delete()

    @commands.command(brief='Converts GBP to CAD')
    async def gbp(self, ctx, num: float):
        converted = await convert_gbp(num)
        await ctx.send('£' + str(num) + ' GBP is {:.2f} CAD'.format(converted))
        await ctx.message.delete()


async def convert_curr(num: float, base: str, dest: str) -> float:
    rate = currencyRates.get_rate(base.strip().upper(), dest.strip().upper())
    return float(num) * float(rate)  # float on num for TypeError


async def convert_usd(num: float) -> float:
    return float(num) * float(currencyRates.get_rate('USD', 'CAD'))


async def convert_eur(num: float) -> float:
    return float(num) * float(currencyRates.get_rate('EUR', 'CAD'))


async def convert_gbp(num: float) -> float:
    return float(num) * float(currencyRates.get_rate('GBP', 'CAD'))
