from mcdreforged import CommandSource, CommandContext

import auto_uuid_api.mcdr.runtime as runtime

from mcdreforged.api.command import SimpleCommandBuilder
from mcdreforged.api.types import PluginServerInterface

builder = SimpleCommandBuilder()
root_command: str = runtime.config.root_command


def register_commands(server: PluginServerInterface):
    builder.register(server)


# noinspection PyUnusedLocal
@builder.command(f"!!{root_command}")
def on_command_main(src: CommandSource, ctx: CommandContext):
    src.reply("auto_uuid_api.command.main")
