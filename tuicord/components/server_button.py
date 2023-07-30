import discord
from discord import ChannelType
from textual import on
from textual.widgets import Button, Tree

from tuicord.utils import format_name


class ServerButton(Button):
    def __init__(self, guild, channel_tree, *args, **kwargs):
        self.client = self.app.client
        self.guild: discord.Guild = guild
        self.channel_tree: Tree = channel_tree
        super().__init__(*args, **kwargs)

    @on(Button.Pressed)
    def button_pressed(self, _: Button.Pressed):
        chat = self.app.query(
            '#category-tree').first()
        chat.clear()
        for channel in self.guild.channels:
            if channel.type == ChannelType.category:
                data = {'channel': channel}
                category_tree = chat.root.add(
                    label=f'[blue]{format_name(channel.name)}[/]', data=data)
                for category_channel in channel.text_channels:
                    data = {'channel': category_channel}
                    category_tree.add_leaf(category_channel.name, data=data)
            elif not channel.category:
                data = {'channel': channel}
                chat.root.add(label=format_name(channel.name), data=data)
        self.app.set_actual_server(self.guild)

    # def on_button_pressed(self, _: Button.Pressed) -> None:
    #     self.app.set_actual_server(self.guild)
    #
    #     if self.channels_tree:
    #         self.channels_tree = self.app.query('#category-tree').first()
    #     self.channels_tree = chat
    #     self.channels_tree.clear()
    #     if self.channels_tree:
    #     for channel in self.guild.channels:
    #         if channel.type == ChannelType.category:
    #             data = {'channel': channel}
    #             category_tree = chat.root.add(
    #                 label=f'[blue]{format_name(channel.name)}[/]', data=data)
    #             for category_channel in channel.text_channels:
    #                 data = {'channel': category_channel}
    #                 category_tree.add_leaf(category_channel.name, data=data)
    #         elif not channel.category:
    #             data = {'channel': channel}
    #             chat.root.add(label=format_name(channel.name), data=data)
    #     self.app.set_actual_server(self.guild)
