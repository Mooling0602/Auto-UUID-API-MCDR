import threading

import auto_uuid_api.mcdr.runtime as runtime

from mcdreforged.api.all import (
    ServerInterface,
    PluginServerInterface,
    new_thread,
    spam_proof,
)
from auto_uuid_api.mcdr.commands import register_commands
from auto_uuid_api.mcdr.config import load_config
from auto_uuid_api.mcdr.utils import get_server_dir
from auto_uuid_api import set_server_dir

__detect_optional_dependency: bool = True
__tr_dependencies_detector: str = ""
__tr_unloaded: str | None = None
psi: PluginServerInterface = ServerInterface.psi()


# noinspection PyUnusedLocal
def on_load(server: PluginServerInterface, _prev_module):
    runtime.__plugin_psi = server
    runtime.config_dir = server.get_data_folder()
    runtime.config = load_config(server)
    register_commands(server)
    server_dir: str | None = get_server_dir(server)
    if server_dir:
        set_server_dir(server_dir, server)
    else:
        server.logger.warning(server.rtr("auto_uuid_api.disable_locally_features"))
        runtime.__disable_locally_features = True
    server.logger.info(server.rtr("auto_uuid_api.loaded"))
    global __tr_dependencies_detector, __tr_unloaded
    __tr_dependencies_detector = str(server.rtr("auto_uuid_api.dependencies_detector"))
    __tr_unloaded = str(server.rtr("auto_uuid_api.unloaded"))
    if server.is_server_running():
        on_server_start(server)


def on_server_start(server: PluginServerInterface):
    assert callable(on_most_plugins_may_loaded)
    on_most_plugins_may_loaded(server)


@new_thread()
@spam_proof()
def on_most_plugins_may_loaded(server: PluginServerInterface):
    threading.current_thread().name = __tr_dependencies_detector
    global __detect_optional_dependency
    if not __detect_optional_dependency:
        return
    __detect_optional_dependency = False
    server.logger.warning(server.rtr("auto_uuid_api.not_implemented"))


def on_unload(server: PluginServerInterface):
    runtime.__plugin_psi = None
    runtime.config_dir = None
    runtime.config = None
    if __tr_unloaded:
        server.logger.info(__tr_unloaded)
