import discord
from textual.widget import Widget
from textual.widgets import ListItem, ListView

from tuicord.components import ChannelMessage


class DiscordClient(discord.Client):
    def __init__(self, **kwargs):
        self.app = None
        super(DiscordClient, self).__init__(**kwargs)

    async def on_ready(self):
        guilds = []
        for guild in self.guilds:
            guilds.append(guild)

        @self.event
        async def on_message(message: discord.Message):
            if not (self.app.actual_channel and self.app.actual_server):
                return
            try:
                if all([
                    message.guild.id == self.app.actual_server.id,
                    message.channel.id == self.app.actual_channel.id]
                ):
                    message_list_view: ListView | Widget = self.app.query(
                        '#message-list').first()

                    await message_list_view.append(ListItem(ChannelMessage(
                        message.channel,
                        f'[{message.author.color}] {message.author} [/]: {message.content}',
                    )))
                    message_list_view.index = len(message_list_view) - 2
            except Exception as error:
                message_list_view: Widget = self.app.query(
                    '#message-list').first()
                await message_list_view.append(
                    ListItem(ChannelMessage(message.channel,
                                            str(error))))
