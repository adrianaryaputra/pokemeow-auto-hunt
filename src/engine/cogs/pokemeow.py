import asyncio, re, time, discord
from discord.ext import commands as BotCmd
from discord.ext import tasks as BotTask
from threading import Thread

from tools.messageBuffer import MessageBuffer
from tools.discordMessageSender import DiscordMsgSend, send as sender

from engine.configurator import cfg
from engine.pokemeow import PokeRarity, PokeRarities, PokeBalls




class PokeMeow(BotCmd.Cog):
    """PokeMeow cogs"""

    def __init__(self, bot: BotCmd.Bot) -> None:
        self.bot = bot
        self.token = cfg.getToken()
        self.catchlock = None
        self.catchlocklimit = 50
        self.catchlockcount = 0
        self.catchlocklimiter.start()
        self.messageBuffer = MessageBuffer()
        self.messageSender.start()

    @BotCmd.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """
        handle incoming message        
        """
        if str(message.author) == "PokéMeow#6691":
            await self.handleCommandP(message)
            await self.handleWaitTime(message)
            await self.handleCaptcha(message)
            await self.handleCaptchaComplete(message)
            return

    @BotCmd.Cog.listener()
    async def on_message_edit(self, old: discord.Message, new: discord.Message) -> None:
        """
        handle message edit
        """
        if str(new.author) != "PokéMeow#6691": return
        await self.handleCommandF(new)

    @BotTask.loop(seconds=0.5)
    async def messageSender(self) -> None:
        """
        send message on cog buffer if it exist
        """
        if not cfg.getPokeMeow(): return
        msg: DiscordMsgSend = self.messageBuffer.get()
        if msg:
            await msg.send()


    @BotCmd.command(pass_context=True)
    async def poke(self, ctx: BotCmd.Context, toggle: str = "", poke_cmd: str = "") -> None:
        """
        send poke command
        """
        togglesel = ["start", "stop", "nick"]
        pokecmdsel = ["p", "f"]
        example = f"example: `$poke {togglesel[0]} {pokecmdsel[0]}`"

        await ctx.message.delete()

        if not cfg.getPokeMeow():
            await ctx.send("PokeMeow is `Disabled`! you should enable it to use this command...")
            return
        if toggle == "":
            await ctx.send(f"you should specify toggle {togglesel}. {example}")
            return
        if toggle not in togglesel:
            await ctx.send(f"toggle should be one of {togglesel}. {example}")
            return
        if toggle == "nick":
            cfg.setNickname(poke_cmd)
            return
        if poke_cmd == "":
            await ctx.send(f"you should specify poke command {pokecmdsel}. {example}")
            return
        if poke_cmd not in pokecmdsel:
            await ctx.send(f"poke command should be one of {pokecmdsel}. {example}")
            return
        if toggle == "start":
            if poke_cmd == "p": 
                self.channelP = ctx.channel
                if not self.loopP.is_running(): self.loopP.start()
            if poke_cmd == "f": 
                self.channelF = ctx.channel
                if not self.loopF.is_running(): self.loopF.start()
        if toggle == "stop":
            if poke_cmd == "p": 
                if self.loopP.is_running(): self.loopP.stop()
                self.channelP = None
            if poke_cmd == "f": 
                if self.loopF.is_running(): self.loopF.stop()
                self.channelF = None



    @BotTask.loop(seconds=cfg.getPokeDelay(2))
    async def loopF(self) -> None:
        """
        handle run f command every duration
        """
        self.sendMessage(";f", self.channelF, lock=";f", nolock=False)
        self.loopF.change_interval(seconds=cfg.getPokeDelay(2))


    @BotTask.loop(seconds=cfg.getPokeDelay(1))
    async def loopP(self) -> None:
        """
        handle run p command every duration
        """
        self.sendMessage(";p", self.channelP, lock=";p", nolock=False)
        self.loopP.change_interval(seconds=cfg.getPokeDelay(1))


    @BotTask.loop(seconds=0.1)
    async def catchlocklimiter(self) -> None:
        if self.catchlock: self.catchlockcount += 1
        else : self.catchlockcount = 0
        if self.catchlockcount >= self.catchlocklimit: 
            self.catchlock = None
            self.catchlockcount = 0


            

    async def handleCommandP(self, message: discord.Message) -> None:

        def _getTargetName(msg: str):
            regex = re.search(r"\*\*(.+)\*\* found a", msg) if msg else None
            return regex.group(1) if regex else None

        def _getPokeRarity(msg: str) -> PokeRarity:
            regex = re.search(PokeRarities.compiledRe(), msg) if msg else None
            regroup = regex.group(1) if regex else None
            return PokeRarities.reg2type(regroup) if regroup else None

        def _getPokeBall(msg: str) -> None:
            m = msg.replace(',', '').replace('.', '') if msg else None
            regex = re.findall(r"balls[ ]*:[ ]*([0-9]+)", m) if m else None
            if len(regex) == 5:
                PokeBalls.Reg.setCount(int(regex[0]))
                PokeBalls.Ultra.setCount(int(regex[1]))
                PokeBalls.Great.setCount(int(regex[2]))
                PokeBalls.Master.setCount(int(regex[3]))
                PokeBalls.Premier.setCount(int(regex[4]))

        targetname = _getTargetName(message.content)
        embed: discord.Embed = message.embeds[0] if message.embeds else None
        if not targetname: return
        if embed.footer: embFootContent = embed.footer.text or None
        rarity = _getPokeRarity(embFootContent)
        if not embFootContent: return
        if not rarity: return
        if targetname != self.bot.user.name: return
        _getPokeBall(embFootContent)
        self.sendMessage(rarity.ball(), message.channel, unlock=True)
        await self.handleBuyBall(message.channel)



    async def handleCommandF(self, message: discord.Message) -> None:
        
        def _getTargetName(msg: str):
            regex = re.search(r"\*\*(.[^<>*]+)\*\* ", msg) if msg else None
            return regex.group(1) if regex else None

        def _getPULL(msg: str):
            regex = re.search(r"(`PULL`)", msg) if msg else None
            return regex.group(1) if regex else None

        def _getPokeName(msg: str) -> str:
            regex = re.search(r"(Kyoigre|Suicune)", msg) if msg else None
            return regex.group(1) if regex else None

        def _getPokeShiny(msg: str) -> bool:
            regex = re.search(r"(Shiny|Golden)", msg) if msg else None
            return regex.group(1) if regex else None

        def _getPokeFished(msg: str) -> str:
            regex = re.search(r"(fished out)", msg) if msg else None
            return regex.group(1) if regex else None

        def _getNibble(msg: str):
            regex = re.search(r"(Not even a nibble)", msg) if msg else None
            return regex.group(1) if regex else None

        def _getRunaway(msg: str):
            regex = re.search(r"(got away)", msg) if msg else None
            return regex.group(1) if regex else None

        pull: str = None
        nibble: str = None
        runaway: str = None
        pokeusedb: str = None
        pokeusemb: str = None
        pokeusegb: str = None

        embed: discord.Embed = message.embeds[0] if message.embeds else None        
        embedname: str = _getTargetName(embed.description) if embed else ''

        if not embedname: return
        if embedname.lower() in [
            str(self.bot.user.name).lower(), 
            cfg.getNickname().lower()
        ]:
            pull = _getPULL(embed.description) if embed else None
            nibble = _getNibble(embed.description) if embed else None
            runaway = _getRunaway(embed.description) if embed else None
            pokeusedb = _getPokeName(embed.description) if embed else None
            pokeusemb = _getPokeShiny(embed.description) if embed else None
            pokeusegb = _getPokeFished(embed.description) if embed else None


        if pull:
            self.sendMessage("pull", message.channel)
            return

        if pokeusedb:
            self.sendMessage("db", message.channel, unlock=True)
            # self.catchlock = False
            return

        if pokeusemb:
            self.sendMessage("mb", message.channel, unlock=True)
            # self.catchlock = False

        if pokeusegb:
            self.sendMessage("gb", message.channel, unlock=True)
            # self.catchlock = False
            return

        if nibble: 
            self.catchlock = False
            return

        if runaway: 
            self.catchlock = False
            return



    async def handleWaitTime(self, message: discord.Message) -> None:

        def _getmatch(msg: str):
            regex = re.search(r"(please wait)", msg) if msg else None
            return regex.group(1) if regex else None

        if not _getmatch(message.content): return
        me = [name for name in message.mentions if name.id == self.bot.user.id]
        if not len(me): return
        if not self.catchlock: return
        rc: str = self.catchlock
        self.catchlock = None




    async def handleCaptcha(self, message: discord.Message) -> None:

        def _getmatch(msg: str):
            regex = re.search(r"(please respond with the number)", msg) if msg else None
            return regex.group(1) if regex else None

        if not _getmatch(message.content): return
        me = [name for name in message.mentions if name.id == self.bot.user.id]
        if not len(me): return
        cfg.setPokeMeow(False)


    async def handleCaptchaComplete(self, message: discord.Message) -> None:

        def _getmatch(msg: str):
            regex = re.search(r"(thank you, you may continue hunting!)", msg) if msg else None
            return regex.group(1) if regex else None

        if not _getmatch(message.content): return
        me = [name for name in message.mentions if name.id == self.bot.user.id]
        if not len(me): return
        cfg.setPokeMeow(True)
        self.catchlock = False



    def sendMessage(self, msg: str, channel: discord.TextChannel, lock: str = None, unlock: bool = False, nolock: bool = True) -> None:

        # don't push if already exist
        if msg in [str(msg) for msg in self.messageBuffer.list()]: return
        if msg == self.catchlock: return

        if not nolock: 
            if self.catchlock: return
        self.messageBuffer.add(sender(msg, channel))
        if lock: self.catchlock = lock
        if unlock: self.catchlock = None




    async def handleBuyBall(self, channel: discord.TextChannel) -> None:
        """
        handle buy ball
        """
        if PokeBalls.Reg.shouldbuy():
            await asyncio.sleep(2)
            self.sendMessage(PokeBalls.Reg.buy(), channel)
        if PokeBalls.Great.shouldbuy():
            await asyncio.sleep(2)
            self.sendMessage(PokeBalls.Great.buy(), channel)
        if PokeBalls.Ultra.shouldbuy():
            await asyncio.sleep(2)
            self.sendMessage(PokeBalls.Ultra.buy(), channel)
        if PokeBalls.Master.shouldbuy():
            await asyncio.sleep(2)
            self.sendMessage(PokeBalls.Master.buy(), channel)




def setup(bot) -> None:
    bot.add_cog(PokeMeow(bot))