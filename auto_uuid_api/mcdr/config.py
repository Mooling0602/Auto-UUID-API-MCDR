from mcdreforged.api.utils import Serializable
from mcdreforged.api.types import PluginServerInterface


class OptionalSupport(Serializable):
    meowtiwhitelist: bool = False


class DefaultConfig(Serializable):
    enable_api: bool = False
    locate_server_dir_by_pid: bool = True
    root_command: str = "auto_uuid_api"
    optional: OptionalSupport = OptionalSupport()


__default_config: DefaultConfig = DefaultConfig()


def load_config(server: PluginServerInterface) -> DefaultConfig:
    __config = server.load_config_simple(
        file_name="config.yml", target_class=DefaultConfig
    )
    if not isinstance(__config, DefaultConfig):
        raise TypeError(server.rtr("auto_uuid_api.config.error"))
    if "meowtiwhitelist" in server.get_plugin_list():
        server.logger.info(server.rtr("auto_uuid_api.detected_meowtiwhitelist"))
        if not __config.optional.meowtiwhitelist:
            server.logger.info(server.rtr("auto_uuid_api.enabling_meowtiwhitelist"))
            __default_config.optional.meowtiwhitelist = True
            server.save_config_simple(config=__default_config, file_name="config.yml")
            _result_config = server.load_config_simple(
                file_name="config.yml",
                target_class=DefaultConfig,
                echo_in_console=False,
            )
            if isinstance(_result_config, DefaultConfig):
                return _result_config
        server.logger.info(server.rtr("auto_uuid_api.config_fine"))
    server.logger.info(server.rtr("auto_uuid_api.load_config_normally"))
    return __config
