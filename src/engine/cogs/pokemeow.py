import asyncio
from random import random
import re
from time import time
import discord
from discord.ext import commands as BotCmd

from ..configurator import cfg



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
        self.limiter = time()
        self.catchlock = None


    @BotCmd.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """
        handle incoming message        
        """

        if not self.enabled:
            print("PokeMeow disabled")
            return

        await self.handleCommandStart(message)

        if str(message.author) != "PokéMeow#6691":
            return

        await self.handleCommandP(message)




    @BotCmd.Cog.listener()
    async def on_message_edit(self, old: discord.Message, new: discord.Message) -> None:
        """
        handle message edit
        """

        if not self.enabled:
            return

        if str(new.author) != "PokéMeow#6691":
            return

        await self.handleCommandF(new)

        

        

    async def handleCommandP(self, message: discord.Message) -> None:

        def _getTargetName(msg: str):
            regex = re.search(r"\*\*(.+)\*\* found a", msg) if msg else None
            return regex.group(1) if regex else None

        targetname = _getTargetName(message.content)

        if not targetname: return

        embed: discord.Embed = message.embeds[0] if message.embeds else None
        embFootContent = None

        if embed.footer: embFootContent = embed.footer.text or None
        if not embFootContent: return

        rarity = self._getPokeRarity(embFootContent)
        
        if not rarity: return
        if targetname != self.bot.user.name: return

        # limiter waiting
        wait = max(1, self.limiter - time())
        await asyncio.sleep(wait)
        self.limiter = time() + 3
        await message.channel.send(rarity.ball())
        self.catchlock = None

        await asyncio.sleep(9 + random()*4)
        wait = max(0, self.limiter - time())
        await asyncio.sleep(wait)
        self.limiter = time() + 3
        l = 0
        while self.catchlock:
            await asyncio.sleep(0.1)
            print(self.catchlock)
            l+=1; 
            if l >= 600: break
        await message.channel.send(";p")
        self.catchlock = ";p"



    async def handleCommandStart(self, message: discord.Message) -> None:
        
        if not self.enabled: return
        if str(message.author) != str(self.bot.user): return

        if message.content.startswith("let's start"):
            await message.channel.send(";p")
            self.catchlock = ";p"
            l = 0
            while self.catchlock:
                await asyncio.sleep(0.1)
                print(self.catchlock)
                l+=1
                if l >= 600: break
            await asyncio.sleep(2)
            await message.channel.send(";f")
            self.catchlock = ";f"



    async def handleCommandF(self, message: discord.Message) -> None:
        
        def _getTargetName(msg: str):
            regex = re.search(r"\*\*(.[^<>]+)\*\* ", msg) if msg else None
            return regex.group(1) if regex else None

        def _getPULL(msg: str):
            regex = re.search(r"(`PULL`)", msg) if msg else None
            return regex.group(1) if regex else None

        def _getCaugth(msg: str):
            regex = re.search(r"^\*\*(.[^<>]+)\*\* (fished out a wild)", msg) if msg else None
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
        # caught: str = _getCaugth(embed.description) if embed else None
        nibble: str = _getNibble(embed.description) if embed else None
        runaway: str = _getRunaway(embed.description) if embed else None

        if pull:
            wait = max(0, self.limiter - time())
            await asyncio.sleep(wait)
            await message.channel.send('pull')
            self.limiter = time() + 1

            wait = max(0, self.limiter - time())
            await asyncio.sleep(wait+random()*1)
            await message.channel.send('gb')
            self.limiter = time() + 2
            caught = 'caught'
            self.catchlock = None

                
        if nibble or runaway or caught:
            await asyncio.sleep(21 + random()*4)
            wait = max(0, self.limiter - time())
            await asyncio.sleep(wait)
            self.limiter = time() + 2
            l = 0
            while self.catchlock:
                await asyncio.sleep(0.1)
                print(self.catchlock)
                l+=1; 
                if l >= 600: break
            await message.channel.send(';f')
            self.catchlock = ";f"
        


    def _getPokeRarity(self, msg: str) -> PokeMeowRarity:
        regex = re.search(PokeMeowRarityType.compiledRe(), msg)
        if regex:
            regroup = regex.group(1)
            return PokeMeowRarityType.reg2type(regroup)
        return None




def setup(bot) -> None:
    bot.add_cog(PokeMeowMeets(bot))