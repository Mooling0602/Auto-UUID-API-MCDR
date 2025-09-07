from typing import Optional
from mcdreforged.api.types import PluginServerInterface
from auto_uuid_api.mcdr.config import DefaultConfig

__plugin_psi: Optional[PluginServerInterface] = None
__disable_locally_features: bool = False
config_dir: Optional[str] = None
config: Optional[DefaultConfig] = None
server_dir: Optional[str] = None
