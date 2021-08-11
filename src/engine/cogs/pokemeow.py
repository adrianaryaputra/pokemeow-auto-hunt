import asyncio
from asyncio.threads import to_thread
from random import random
import re
import time
import discord
from discord.ext import commands as BotCmd
from discord.ext import tasks as BotTask
from threading import Thread

from ..configurator import cfg
from tools.messageBuffer import MessageBuffer
from tools.discordMessageSender import DiscordMsgSend, send as sender



class PokeMeowRarity:
    def __init__(self, regex, rarity, balls) -> None:
        self.regex = regex
        self.rarity = rarity
        self.balls = balls

    def __str__(self) -> str:
        return self.rarity

    def re(self) -> str:
        return self.regex

    def ball(self) -> str:
        return self.balls




class PokeMeowRarityType:
    COMMON: PokeMeowRarity = PokeMeowRarity(r"Common", "Common", "gb")
    UNCOMMON: PokeMeowRarity = PokeMeowRarity(r"Uncommon", "Uncommon", "gb")
    RARE: PokeMeowRarity = PokeMeowRarity(r"Rare", "Rare", "gb")
    SHINYF: PokeMeowRarity = PokeMeowRarity(r"Shiny \(F", "Shiny Full", "gb")
    SUPERRARE: PokeMeowRarity = PokeMeowRarity(r"Super Rare", "Super Rare", "ub")
    LEGENDARY: PokeMeowRarity = PokeMeowRarity(r"Legendary", "Legendary", "mb")
    SHINYA: PokeMeowRarity = PokeMeowRarity(r"Shiny \(A", "Shiny Approx", "mb")
    SHINYE: PokeMeowRarity = PokeMeowRarity(r"Shiny \(E", "Shiny Exact", "mb")

    @classmethod
    def compiledRe(self) -> str:
        return r"({})".format("|".join([r.re() for r in [
            self.COMMON,
            self.UNCOMMON,
            self.RARE,
            self.SHINYF,
            self.SUPERRARE,
            self.LEGENDARY,
            self.SHINYA,
            self.SHINYE
        ]]))

    @classmethod
    def reg2type(self, reg: str) -> str:
        for r in [
            self.COMMON, 
            self.UNCOMMON, 
            self.RARE, 
            self.SHINYF, 
            self.SUPERRARE, 
            self.LEGENDARY, 
            self.SHINYA, 
            self.SHINYE
        ]:
            if re.match(r.re(), reg):
                return r
        return None




class PokeMeowMeets(BotCmd.Cog):
    """PokeMeow cogs"""

    def __init__(self, bot: BotCmd.Bot) -> None:
        self.bot = bot
        self.token = cfg.getToken()
        self.enabled = cfg.getPokeMeow()
        self.catchlock = None
        self.messageBuffer = MessageBuffer()
        self.messageSender.start()


    @BotCmd.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """
        handle incoming message        
        """
        if not self.enabled: return
        await self.handleCommandStart(message)
        if str(message.author) != "PokéMeow#6691": return
        await self.handleCommandP(message)
        await self.handleWaitTime(message)
        await self.handleCaptcha(message)




    @BotCmd.Cog.listener()
    async def on_message_edit(self, old: discord.Message, new: discord.Message) -> None:
        """
        handle message edit
        """
        if not self.enabled: return
        if str(new.author) != "PokéMeow#6691": return
        await self.handleCommandF(new)


    

    @BotTask.loop(seconds=2)
    async def messageSender(self) -> None:
        """
        send message on cog buffer if it exist
        """
        if not self.enabled: return
        msg: DiscordMsgSend = self.messageBuffer.get()
        print("catch lock: " + self.catchlock) if self.catchlock else None
        if msg: 
            print(f"sending message: {msg}")
            await msg.send()

        

        

    async def handleCommandP(self, message: discord.Message) -> None:

        def _getTargetName(msg: str):
            regex = re.search(r"\*\*(.+)\*\* found a", msg) if msg else None
            return regex.group(1) if regex else None

        def _getPokeRarity(msg: str) -> PokeMeowRarity:
            regex = re.search(PokeMeowRarityType.compiledRe(), msg) if msg else None
            regroup = regex.group(1) if regex else None
            return PokeMeowRarityType.reg2type(regroup) if regroup else None

        targetname = _getTargetName(message.content)
        embed: discord.Embed = message.embeds[0] if message.embeds else None
        if not targetname: return
        if embed.footer: embFootContent = embed.footer.text or None
        rarity = _getPokeRarity(embFootContent)
        if not embFootContent: return
        if not rarity: return
        if targetname != self.bot.user.name: return
        self.sendMessage(rarity.ball(), message.channel, unlock=True)
        await asyncio.sleep(9 + random()*4)
        self.sendMessage(";p", message.channel, lock=";p", nolock=False)



    async def handleWaitTime(self, message: discord.Message) -> None:

        def _getmatch(msg: str):
            regex = re.search(r"(please wait)", msg) if msg else None
            return regex.group(1) if regex else None

        if not self.enabled: return
        if not _getmatch(message.content): return
        me = [name for name in message.mentions if name.id == self.bot.user.id]
        if not len(me): return
        print("caught waiting")
        if not self.catchlock: return
        rc: str = self.catchlock
        self.catchlock = None
        print("reset catchlock")
        await asyncio.sleep(20 + random()*3)
        self.sendMessage(rc, message.channel, lock=rc, nolock=False)




    async def handleCaptcha(self, message: discord.Message) -> None:

        def _getmatch(msg: str):
            regex = re.search(r"(please respond with the number)", msg) if msg else None
            return regex.group(1) if regex else None

        if not self.enabled: return
        if not _getmatch(message.content): return
        me = [name for name in message.mentions if name.id == self.bot.user.id]
        if not len(me): return
        self.catchlock = None
        await asyncio.sleep(1)
        self.messageBuffer.flush()

        



    async def handleCommandStart(self, message: discord.Message) -> None:
        if not self.enabled: return
        if str(message.author) != str(self.bot.user): return
        if message.content.startswith("let's start"):
            print("=== LET'S START DETECTED ===")
            self.sendMessage(";p", message.channel, lock=";p", nolock=False)
            self.sendMessage(";f", message.channel, lock=";f", nolock=False)



    async def handleCommandF(self, message: discord.Message) -> None:
        
        def _getTargetName(msg: str):
            regex = re.search(r"\*\*(.[^<>]+)\*\* ", msg) if msg else None
            return regex.group(1) if regex else None

        def _getPULL(msg: str):
            regex = re.search(r"(`PULL`)", msg) if msg else None
            return regex.group(1) if regex else None

        def _getNibble(msg: str):
            regex = re.search(r"(Not even a nibble)", msg) if msg else None
            return regex.group(1) if regex else None

        def _getRunaway(msg: str):
            regex = re.search(r"(got away)", msg) if msg else None
            return regex.group(1) if regex else None

        embed: discord.Embed = message.embeds[0] if message.embeds else None        
        targetname: str = _getTargetName(embed.description) if embed else ''
        if targetname != self.bot.user.name: return
        pull: str = _getPULL(embed.description) if embed else None
        nibble: str = _getNibble(embed.description) if embed else None
        runaway: str = _getRunaway(embed.description) if embed else None

        if pull:
            self.sendMessage("pull", message.channel)
            self.sendMessage("gb", message.channel, unlock=True)
            caught = 'caught'

        if nibble or runaway or caught:
            await asyncio.sleep(21 + random()*4)
            self.sendMessage(";f", message.channel, lock=";f", nolock=False)



    def sendMessage(self, msg: str, channel: discord.TextChannel, lock: str = None, unlock: bool = False, nolock: bool = True) -> None:

        # don't push if already exist
        print(self.messageBuffer.list())
        if msg in [str(msg) for msg in self.messageBuffer.list()]: return
        if msg == self.catchlock: return

        def _sendmsg():
            print("=== SENDING MESSAGE ===")
            l = 0
            if not nolock: 
                while self.catchlock:
                    time.sleep(0.5)
                    l+=1
                    if l >= 40: self.catchlock = None
            print(f"add message to Buffer: {msg}")
            self.messageBuffer.add(sender(msg, channel))
            if lock: self.catchlock = lock
            if unlock: self.catchlock = None

        Thread(target=_sendmsg).start()




def setup(bot) -> None:
    bot.add_cog(PokeMeowMeets(bot))