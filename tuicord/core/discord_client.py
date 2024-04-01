import discord
from textual.widget import Widget
from textual.widgets import ListItem, ListView

from tuicord.components import ChannelMessage


class DiscordClient(discord.Client):
    def __init__(self, **kwargs):
        """
        The __init__ function is called when the class is instantiated.
        It sets up all the attributes that will be used by other functions
        in the class.


        :param self: Represent the instance of the class
        :param **kwargs: Pass a variable number of keyword arguments to the
        function
        :return: None
        """
        self.app = None
        super(DiscordClient, self).__init__(**kwargs)

    async def on_ready(self):
        """
        The on_ready function is called when the bot has finished logging in
        and setting up.

        :param self: Represent the instance of the class
        :return: A list of guilds
        """

        @self.event
        async def on_message(message: discord.Message):
            """
            The on_message function is a coroutine that will be called whenever
            a message is sent in a channel.
            It takes one argument, which is the message object itself.
            The message object has many attributes and methods,
            but we're only going to use two of them: author and content.
            The author attribute is a Member object representing who sent the
            message, while content represents the actual contents of the
            message.

            :param message: discord.Message: Get the message that was sent
            :return: None
            """
            if not (self.app.actual_channel and self.app.actual_server):
                return
            try:
                if all(
                    [
                        message.guild.id == self.app.actual_server.id,
                        message.channel.id == self.app.actual_channel.id,
                    ]
                ):
                    message_list_view: ListView | Widget = self.app.query(
                        '#message-list'
                    ).first()

                    await message_list_view.append(
                        ListItem(
                            ChannelMessage(
                                message.channel,
                                f'[{message.author.color}] {message.author} [/]: {message.content}',
                            )
                        )
                    )
                    message_list_view.index = len(message_list_view) - 2
            except Exception as error:
                message_list_view: Widget = self.app.query(
                    '#message-list'
                ).first()
                await message_list_view.append(
                    ListItem(ChannelMessage(message.channel, str(error)))
                )
