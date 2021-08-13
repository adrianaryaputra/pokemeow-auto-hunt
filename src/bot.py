from engine.configurator import cfg
from tools.formatcmd import dateprint
from discord.ext import commands as BotCmd
from datetime import datetime


def loadCogs(bot):
    bot.load_extension("engine.cogs.main")
    bot.load_extension("engine.cogs.nitro")
    bot.load_extension("engine.cogs.pokemeow")



if __name__ == '__main__':

    print("====================================")
    print("   Welcome to PokeMeow Sniper Bot   ")
    print("           Farabot © 2021           ")
    print("====================================")
    print("")
    print("")
    dateprint("checking token...")
    tokenValid = cfg.checkToken()
    if not tokenValid: cfg.handleInvalidToken(cfg.getToken())
    dateprint("initializing...")
    dateprint("this may take a few second...")

    bot = BotCmd.Bot(command_prefix=cfg.getPrefix(), self_bot=True)
    bot.remove_command('help')

    @bot.event
    async def on_ready():
        dateprint("bot is ready!")
        loadCogs(bot)
    
    bot.run(cfg.getToken())

    


