import discord
from textual.widgets import Label


class ChannelMessage(Label):
    def __init__(self, channel: discord.TextChannel, *args, **kwargs):
        self.channel = channel
        self.channel_id = channel.id
        super(ChannelMessage, self).__init__(*args, **kwargs)
