from mcdreforged.api.types import PluginServerInterface
from auto_uuid_api.mcdr.config import DefaultConfig

__plugin_psi: PluginServerInterface | None = None
__disable_locally_features: bool = False
config_dir: str | None = None
config: DefaultConfig | None = None
