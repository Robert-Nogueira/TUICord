import asyncio

import discord
from discord import ChannelType
from textual import on
from textual.widget import Widget
from textual.widgets import ListItem, ListView, Tree

from tuicord.components.channel_message import ChannelMessage
from tuicord.utils import consume_history, format_name


class ChannelsTree(Tree):
    def __init__(self, guild: discord.Guild, *args, **kwargs):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines all attributes that
        will be used by instances of this class.

        :param self: Refer to the current instance of a class
        :param guild: discord.Guild: Set the guild attribute of the class
        :param *args: Pass a non-keyword, variable-length argument list to the
        function
        :param **kwargs: Pass keyword arguments to the superclass
        :return: None
        """
        self.guild = guild
        super().__init__(*args, **kwargs)

    def on_mount(self):
        """
        The on_mount function is called when the tree is first mounted.
        It's a good place to add all of your top-level nodes, as well as any
        other initialization you need to do.

        :param self: Refer to the current instance of a class
        :return: None
        """
        for channel in self.guild.channels:
            if channel.type == ChannelType.category:
                data = {'channel': channel}
                category_tree = self.root.add(
                    label=f'[blue]{format_name(channel.name)}[/]', data=data
                )
                for category_channel in channel.text_channels:
                    data = {'channel': category_channel}
                    category_tree.add_leaf(category_channel.name, data=data)
            elif not channel.category:
                data = {'channel': channel}
                self.root.add(label=format_name(channel.name), data=data)

    @on(Tree.NodeSelected)
    async def on_node_selected(self, event: Tree.NodeSelected):
        """
        The on_node_selected function is called when a node in the tree view
        is selected.

        :param self: Refer to the instance of the class
        :param event: Tree.NodeSelected: Get the node that was selected
        :return: None
        """
        if event.node.is_root:
            return
        channel: discord.TextChannel = event.node.data.get('channel')
        if not isinstance(channel, discord.CategoryChannel):
            self.app.set_actual_channel(channel)
            message_list_view: ListView | Widget = self.app.query(
                '#message-list'
            ).first()
            await message_list_view.clear()
            try:
                messages = asyncio.run_coroutine_threadsafe(
                    consume_history(channel), loop=self.app.client.loop
                ).result()
                for message in messages:
                    await message_list_view.append(
                        ListItem(
                            ChannelMessage(
                                channel,
                                f'[{message.author.color}] {message.author.name}[/]: {message.content}',
                            )
                        )
                    )
                message_list_view.index = len(message_list_view) - 2
            except discord.Forbidden:
                await message_list_view.append(
                    ListItem(
                        ChannelMessage(channel, 'Sem permissão para leitura')
                    )
                )
            except Exception as error:
                await message_list_view.append(
                    ListItem(ChannelMessage(channel, str(error)))
                )
            self.app.set_actual_channel(channel)
