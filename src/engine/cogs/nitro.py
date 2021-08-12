import re
import requests
import discord
from discord.ext import commands as BotCmd

from ..configurator import cfg


class Nitro(BotCmd.Cog):
    """Nitro commands detector"""

    def __init__(self, bot: BotCmd.Bot) -> None:
        self.bot = bot
        self.token = cfg.getToken()


    @BotCmd.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """
        handle incoming message        
        """

        # if nitro is disabled
        if not cfg.getNitro():
            print("nitro disabled")
            return

        # find nitro gift regex
        reggrp = self._findNitroGiftRe(message.content)

        # if nitro gift regex found
        if len(reggrp) == 16 or len(reggrp) == 24:
            claim = await self._claimCode(reggrp)
            print(claim)



    def _clientHeaders(self):
        return {
            'Authorization': self.token,
            'Content-Type': 'application/json',
        }



    def _findNitroGiftRe(self, msgcontent: str) -> str:
        """
        find nitro gift regex
        """

        regex = re.search(r'(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)', msgcontent)
        if regex:
            return regex.group(2)
        return ''

    

    async def _claimCode(self, code: str):
        r = requests.post(f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem',headers=self._clientHeaders(), json={'channel_id': None, 'payment_source_id': None})
        if 'subscription_plan' not in r.text:
            try:
                message = r.json()['message']
            except (AttributeError, IndexError, KeyError):
                message = "cloudflare"
            return {'valid': False, 'message': message, 'code': code}
        else:
            return {'valid': True, 'message': r.json(), 'code': code}



def setup(bot) -> None:
    bot.add_cog(Nitro(bot))