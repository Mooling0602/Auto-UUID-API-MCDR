import auto_uuid_api.mcdr.runtime as runtime

from mcdreforged.api.all import PluginServerInterface
from auto_uuid_api.mcdr.config import load_config
from auto_uuid_api.mcdr.utils import get_server_dir
from auto_uuid_api import set_server_dir


def import_command(server: PluginServerInterface):
    if not runtime.config.root_command:
        server.logger.error("auto_uuid_api.config_error")
        server.unload_plugin(server.get_self_metadata().id)
    from auto_uuid_api.mcdr.commands import register_commands

    register_commands(server)


# noinspection PyUnusedLocal
def on_load(server: PluginServerInterface, _prev_module):
    runtime.__plugin_psi = server
    runtime.config_dir = server.get_data_folder()
    runtime.config = load_config(server)
    import_command(server)
    server_dir = get_server_dir(server)
    if server_dir:
        set_server_dir(server_dir)
    else:
        server.logger.warning("auto_uuid_api.disable_locally_features")
        runtime.__disable_locally_features = True
    server.logger.info("auto_uuid_api.loaded")


def on_unload(server: PluginServerInterface):
    runtime.__plugin_psi = None
    runtime.config_dir = None
    runtime.config = None
    server.logger.info("auto_uuid_api.unloaded")
