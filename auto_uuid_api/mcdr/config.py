from mcdreforged.api.utils import Serializable
from mcdreforged.api.types import PluginServerInterface


class OptionalSupport(Serializable):
    meowtiwhitelist: bool = False  # 检测到此插件已安装并正在工作时，将自动启用


class DefaultConfig(Serializable):
    enable_api: bool = False  # 应由任意下游插件调用时启用
    locate_server_dir_by_pid: bool = True  # 仅在其他方式获取不到服务器路径时才会使用，若设为False，则插件将放弃此方式并直接报错
    root_command: str = "auto_uuid_api"
    optional: OptionalSupport = OptionalSupport()


__default_config: DefaultConfig = DefaultConfig()


def load_config(server: PluginServerInterface) -> DefaultConfig:
    __config: DefaultConfig = server.load_config_simple(
        file_name="config.yml", target_class=DefaultConfig
    )
    if "meowtiwhitelist" in server.get_plugin_list():
        server.logger.debug("auto_uuid_api.detected_meowtiwhitelist")
        if not __config.optional.meowtiwhitelist:
            server.logger.debug("auto_uuid_api.enabling_meowtiwhitelist")
            __default_config.optional.meowtiwhitelist = True
            server.save_config_simple(config=__default_config, file_name="config.yml")
            return server.load_config_simple(
                file_name="config.yml", target_class=DefaultConfig
            )
        server.logger.debug("auto_uuid_api.config_fine")
    server.logger.debug("auto_uuid_api.load_config_normally")
    return __config
