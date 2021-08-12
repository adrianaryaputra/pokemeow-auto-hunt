import asyncio
import discord


class DiscordMsgSend:
    """message to send pack"""
    
    def __init__(self, channel: discord.TextChannel, message: str) -> None:
        self.channel: discord.TextChannel = channel
        self.message: str = message

    def __str__(self) -> str:
        return self.message

    async def send(self) -> None:
        msg = await self.channel.send(self.message)
        # await asyncio.sleep(0.3)
        # await msg.delete()


def send(message: str, channel: discord.TextChannel) -> DiscordMsgSend:
    return DiscordMsgSend(channel, message)