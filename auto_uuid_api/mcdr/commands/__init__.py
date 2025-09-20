import os
import shutil

import auto_uuid_api.mcdr.runtime as runtime

from mcdreforged.api.command import SimpleCommandBuilder, Text, CommandContext
from mcdreforged.api.types import PluginServerInterface, CommandSource

from auto_uuid_api import local_api

builder = SimpleCommandBuilder()
__remove_config_dir: bool = False


def get_server(src: CommandSource) -> PluginServerInterface:
    server: PluginServerInterface | None = None
    if runtime.__plugin_psi:
        server = runtime.__plugin_psi
    else:
        server = src.get_server().psi()
    if server is None:
        raise RuntimeError("Could not found available PluginServerInterface instance.")
    return server


def register_commands(server: PluginServerInterface):
    builder.arg("player", Text)
    builder.arg("uuid", Text)
    if runtime.config:
        builder.command(f"!!{runtime.config.root_command}", on_main_command)
        builder.command(
            f"!!{runtime.config.root_command} get uuid <player>", on_get_uuid
        )
        builder.command(
            f"!!{runtime.config.root_command} get player <uuid>", on_get_player
        )
        builder.command(f"!!{runtime.config.root_command} reload", on_reload_config)
        builder.command(f"!!{runtime.config.root_command} reset", on_clean_config)
    builder.register(server)


# noinspection PyUnusedLocal
def on_main_command(src: CommandSource, ctx: CommandContext):
    src.reply("auto_uuid_api.command.main")


def on_get_uuid(src: CommandSource, ctx: CommandContext) -> str | None:
    player: str | None = ctx.get("player")
    if player:
        result: str | None = local_api.get(player)
        if result:
            src.reply(result)
            return result
    return None


def on_get_player(src: CommandSource, ctx: CommandContext) -> str | None:
    uuid: str | None = ctx.get("uuid")
    if uuid:
        result: str | None = local_api.get(uuid)
        if result:
            src.reply(result)
            return result
        return None


def on_reload_config(src: CommandSource, ctx: CommandContext):
    server: PluginServerInterface = get_server(src)
    server.reload_plugin(server.get_self_metadata().id)


def on_clean_config(src: CommandSource, ctx: CommandContext):
    server: PluginServerInterface = get_server(src)
    if not src.has_permission(4):
        src.reply(server.rtr("auto_uuid_api.permission_denied"))
    global __remove_config_dir
    if not __remove_config_dir:
        src.reply(server.rtr("auto_uuid_api.clean_config.confirm"))
        __remove_config_dir = True
        return
    config_dir = server.get_data_folder()
    if os.path.exists(config_dir):
        try:
            shutil.rmtree(config_dir)
            if not os.path.exists(config_dir):
                src.reply(server.rtr("auto_uuid_api.clean_config.success"))
            else:
                src.reply(server.rtr("auto_uuid_api.clean_config.failed"))
        except Exception as e:
            src.reply(server.rtr("auto_uuid_api.clean_config.failed"))
            raise e
