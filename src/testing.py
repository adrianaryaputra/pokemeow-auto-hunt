from engine.configurator import cfg
from tools.observable import BasicSubscriber

from discord.ext import commands as BotCmd



def loadCogs(bot):
    bot.load_extension("engine.cogs.nitro")
    bot.load_extension("engine.cogs.pokemeow")



if __name__ == '__main__':
    
    bs = BasicSubscriber()
    cfg.registerSub(bs)

    cfg.checkToken()
    print(cfg.getToken())
    print(cfg.getPrefix())
    print(cfg.getNitro())
    print(cfg.getGiveaway())
    print(cfg.getPokeMeow())

    cfg.setNitro(True)
    cfg.setGiveaway(True)
    cfg.setPokeMeow(True)


    bot = BotCmd.Bot(command_prefix=cfg.getPrefix(), self_bot=True)
    bot.remove_command('help')


    @bot.event
    async def on_ready():
        print("bot is ready")
        loadCogs(bot)
    
    bot.run(cfg.getToken())

    


