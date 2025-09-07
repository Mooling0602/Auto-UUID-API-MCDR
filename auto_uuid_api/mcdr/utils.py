import os
import psutil

from typing import List, Tuple, Optional
from mcdreforged.api.types import PluginServerInterface


def get_server_dir(server: PluginServerInterface) -> Optional[str]:
    # 首先搜索白名单文件，然后搜索用户缓存
    target_files = ["whitelist.json", "usercache.json"]
    target_directory = server.get_mcdr_config().get("working_directory", "server")

    def _check_needed_files(files: List[str], directory: str) -> Tuple[bool, bool]:
        _target_count = len(files)
        _matched_count = 0
        for i in files:
            if os.path.exists(os.path.join(directory, i)):
                _matched_count += 1
        if _matched_count > 0:
            if _matched_count < _target_count:
                return True, False
            return True, True
        else:
            return False, False

    _matched, _full_matched = _check_needed_files(target_files, target_directory)
    if _matched:
        if not _full_matched:
            server.logger.warning("auto_uuid_api.missing_some_files")
        return target_directory
    else:
        server_pid = server.get_server_pid()
        server_dir = psutil.Process(server_pid).cwd()
        __matched, __full_matched = _check_needed_files(target_files, server_dir)
        if __matched:
            if not __full_matched:
                server.logger.warning("auto_uuid_api.missing_some_files")
            return server_dir
        else:
            return None
