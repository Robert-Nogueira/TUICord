import discord
from textual.app import App
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, ListView, Footer

from tuicord.components import ServerButton, ChannelsTree
from tuicord.components.input_box import InputBox
from tuicord.utils import format_name


class Interface(App):
    CSS_PATH = 'styles/style.css'
    BINDINGS = [
        ('t', 'change_theme()', 'Muda o tema!'),
        ('s', 'exit()', 'Sai da aplicação!')
    ]

    def __init__(self, client, *args, **kwargs):
        self.client = client
        self.client.app = self
        self._actual_server: discord.Guild | None = None
        self._actual_channel: discord.TextChannel | None = None
        super().__init__(*args, **kwargs)

    @property
    def actual_server(self):
        return self._actual_server

    @property
    def actual_channel(self):
        return self._actual_channel

    def set_actual_server(self, actual_server: discord.Guild):
        self._actual_server = actual_server
        return self._actual_server

    def set_actual_channel(self, actual_channel: discord.TextChannel):
        self._actual_channel = actual_channel
        return self._actual_channel

    def compose(self):
        yield Header()
        with Horizontal():
            with ScrollableContainer(id='sidebar') as sd:
                guilds = [guild for guild in self.client.guilds]
                first_guild = None
                for guild in guilds:
                    tree = ChannelsTree(guild, label='channels',
                                        id='category-tree', data={})
                    tree.root.expand()
                    server_button = ServerButton(label=format_name(guild.name),
                                                 guild=guild,
                                                 channel_tree=tree,
                                                 classes='server-button')
                    if not first_guild:
                        first_guild = server_button
                        self.set_actual_server(guild)
                    yield server_button
            first_category_tree = first_guild.channel_tree
            yield first_category_tree
            with Vertical(id='chat-container'):
                yield ListView(id='message-list')
                yield InputBox(id='text-box')
            # yield Placeholder()
        yield Footer()

    def action_change_theme(self):
        self.dark: bool = not self.dark

    def action_exit(self):
        self.exit()
