import discord
from discord import ChannelType
from textual import on
from textual.widgets import Button, Tree

from tuicord.utils import format_name


class ServerButton(Button):
    def __init__(self, guild, channel_tree, *args, **kwargs):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines all of its
        attributes.
        The first argument to __init__ must always be self, which refers to
        the instance being created.

        :param self: Represent the instance of the class
        :param guild: Get the guild object from discord
        :param channel_tree: Store the channel tree
        :param *args: Send a non-keyword variable length argument list to the
        function
        :param **kwargs: Pass keyword arguments to the function
        :return: None
        """
        self.client = self.app.client
        self.guild: discord.Guild = guild
        self.channel_tree: Tree = channel_tree
        super().__init__(*args, **kwargs)

    @on(Button.Pressed)
    def button_pressed(self, _: Button.Pressed):
        """
        The button_pressed function is called when the user clicks on a server
        in the list of servers.
        It clears all channels from the channel tree, then adds all categories
        and text channels to it.
        Finally, it sets self.app's actual_server attribute to this server.

        :param self: Refer to the current instance of the class
        :param _: Button.Pressed: Tell the function that it will receive a
        button
        :return: None
        """
        chat = self.app.query('#category-tree').first()
        chat.clear()
        for channel in self.guild.channels:
            if channel.type == ChannelType.category:
                data = {'channel': channel}
                category_tree = chat.root.add(
                    label=f'[blue]{format_name(channel.name)}[/]', data=data
                )
                for category_channel in channel.text_channels:
                    data = {'channel': category_channel}
                    category_tree.add_leaf(category_channel.name, data=data)
            elif not channel.category:
                data = {'channel': channel}
                chat.root.add(label=format_name(channel.name), data=data)
        self.app.set_actual_server(self.guild)
