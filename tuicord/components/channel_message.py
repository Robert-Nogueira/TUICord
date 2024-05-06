import discord
from textual.widgets import Label


class ChannelMessage(Label):
    def __init__(
        self, channel: discord.TextChannel, content: str, *args, **kwargs
    ):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the object with all of its attributes and behaviors.
        In this case, it takes in a channel as an argument, and assigns that
        to self.channel.

        :param self: Represent the instance of the object itself
        :param channel: discord.TextChannel: Set the channel attribute of the
        class
        :param *args: Send a non-keyword variable length argument list to the
        function
        :param **kwargs: Pass a variable number of keyword arguments to the
        function
        :return: None
        """
        self.channel = channel
        self.channel_id = channel.id
        self.content = content
        super(ChannelMessage, self).__init__(content, *args, **kwargs)
