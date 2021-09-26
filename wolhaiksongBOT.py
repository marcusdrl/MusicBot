import discord
from discord.ext import commands
import time
from decouple import config
from bot_config import MainCog

bot_exec = commands.Bot(command_prefix='!')
bot_exec.load_extension("bot_config")

bot = MainCog(bot_exec)


@bot_exec.event
async def on_ready():
    print('Logged as: {0.user}'.format(bot_exec))


@bot_exec.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        await ctx.channel.send("```Houve um erro -> O comando não existe```")
    elif isinstance(error, discord.ext.commands.TooManyArguments):
        await ctx.channel.send("```Houve um erro -> Muitos argumentos para play."
                               "\nExemplo de como chamar o comando: !play URL```")

bot_exec.run(config('TOKEN'))
