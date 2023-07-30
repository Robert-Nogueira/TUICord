import asyncio

import discord
from discord import ChannelType
from textual import on
from textual.widget import Widget
from textual.widgets import Tree, ListItem, ListView

from tuicord.components.channel_message import ChannelMessage
from tuicord.utils import consume_history, format_name


class ChannelsTree(Tree):
    def __init__(self, guild: discord.Guild, *args, **kwargs):
        self.guild = guild
        super().__init__(*args, **kwargs)

    def on_mount(self):
        for channel in self.guild.channels:
            if channel.type == ChannelType.category:
                data = {'channel': channel}
                category_tree = self.root.add(
                    label=f'[blue]{format_name(channel.name)}[/]',
                    data=data)
                for category_channel in channel.text_channels:
                    data = {'channel': category_channel}
                    category_tree.add_leaf(category_channel.name,
                                           data=data)
            elif not channel.category:
                data = {'channel': channel}
                self.root.add(label=format_name(channel.name), data=data)

    @on(Tree.NodeSelected)
    async def on_node_selected(self, event: Tree.NodeSelected):
        if event.node.is_root:
            return
        channel: discord.TextChannel = event.node.data.get('channel')
        if not isinstance(channel, discord.CategoryChannel):
            self.app.set_actual_channel(channel)
            message_list_view: ListView | Widget = self.app.query(
                '#message-list').first()
            await message_list_view.clear()
            try:
                messages = asyncio.run_coroutine_threadsafe(
                    consume_history(channel),
                    loop=self.app.client.loop).result()
                for message in messages:
                    await message_list_view.append(ListItem(ChannelMessage(
                        channel,
                        f'[{message.author.color}] {message.author.name}[/]: {message.content}',
                    )))
                message_list_view.index = len(message_list_view) - 2
            except discord.Forbidden:
                await message_list_view.append(
                    ListItem(
                        ChannelMessage(channel, 'Sem permissão para leitura')))
            except Exception as error:
                await message_list_view.append(
                    ListItem(ChannelMessage(channel, str(error))))
            self.app.set_actual_channel(channel)
