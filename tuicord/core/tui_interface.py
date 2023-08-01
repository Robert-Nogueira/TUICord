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
        """
        The __init__ function is called when the class is instantiated.
        It sets up the client and super() calls to set up the cog itself.

        :param self: Represent the instance of the class
        :param client: Pass the client object to the class
        :param *args: Pass a variable number of arguments to the function
        :param **kwargs: Pass in keyword arguments to the function
        :return: None
        """
        self.client = client
        self.client.app = self
        self._actual_server: discord.Guild | None = None
        self._actual_channel: discord.TextChannel | None = None
        super().__init__(*args, **kwargs)

    @property
    def actual_server(self):
        """
        The actual_server function returns the actual server .

        :param self: Represent the instance of the class
        :return: The _actual_server attribute of the class
        """
        return self._actual_server

    @property
    def actual_channel(self):
        """
        The actual_channel function returns the actual channel that the client
        is currently in.

        :param self: Represent the instance of the class
        :return: The _actual channel attribute of the class
        """
        return self._actual_channel

    def set_actual_server(self, actual_server: discord.Guild):
        """
        The set_actual_server function sets the actual server of the client.
        It takes a discord.Guild object as an argument and returns it.

        :param self: Represent the instance of the class
        :param actual_server: discord.Guild: Set the actual server
        :return: The _actual_server
        """
        self._actual_server = actual_server
        return self._actual_server

    def set_actual_channel(self, actual_channel: discord.TextChannel):
        """
        The set_actual_channel function sets the actual channel of the client.
        It takes a discord.TextChannel object as an argument and returns it.

        :param self: Represent the instance of the class
        :param actual_channel: discord.TextChannel: Set the actual channel of
        the client.
        :return: The _actual_channel
        """
        self._actual_channel = actual_channel
        return self._actual_channel

    def compose(self):
        """
        The compose function is the main entry point for a component.
        It defines the layout of the component and returns it as a generator.
        The returned value can be any iterable, but most commonly it's just a
        list or tuple.
        Each item in this iterable will be rendered to HTML and added to the
        DOM tree of your page.

        :param self: Refer to the current instance of a class
        :return: A generator, and the generator yields widgets
        """
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
        """
        The action_change_theme function changes the theme of the application.

        :param self: Refer to the instance of the class
        :return: None
        """
        self.dark: bool = not self.dark

    def action_exit(self):
        """
        The action_exit function is called when the user clicks on the
        &quot;Exit&quot; menu item.
        It closes all windows and exits the program.

        :param self: Represent the instance of the class
        :return: The exit function which is a built-in function
        """
        self.exit()
