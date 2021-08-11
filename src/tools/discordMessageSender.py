import discord


class DiscordMsgSend:
    """message to send pack"""
    
    def __init__(self, channel: discord.TextChannel, message: str) -> None:
        self.channel: discord.TextChannel = channel
        self.message: str = message

    def __str__(self) -> str:
        return self.message

    async def send(self) -> None:
        await self.channel.send(self.message)


def send(message: str, channel: discord.TextChannel) -> DiscordMsgSend:
    return DiscordMsgSend(channel, message)