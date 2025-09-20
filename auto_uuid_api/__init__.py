import json
import os
import re
import uuid

from typing import Literal

from mcdreforged.api.types import PluginServerInterface

server_dir: str | None = None
server: PluginServerInterface | None = None
query_type = Literal["auto", "get_uuid", "get_player", "invalid"]
query_target = Literal["uuid", "player"]


def set_server_dir(_dir: str, _server: PluginServerInterface | None = None):
    global server_dir, server
    server_dir = _dir
    if _server:
        server = _server


def is_uuid(input: str) -> bool:
    try:
        return uuid.UUID(input) is not None
    except Exception:
        return False


class LocallyQuery:
    def __init__(self):
        self.type: query_type = "auto"

    def get(self, content: str) -> str | None:
        self.type = self.get_content_type(content)
        if self.type == "get_player":
            return self.get_player(content)
        elif self.type == "get_uuid":
            return self.get_uuid(content)
        else:
            return None

    def get_content_type(
        self, content: str, regex: str | None = r"\w{3,16}"
    ) -> Literal["get_player", "invalid", "get_uuid"]:
        if is_uuid(content):
            return "get_player"
        elif regex is None:
            return "get_uuid"
        elif re.match(regex, content):
            return "get_uuid"
        else:
            return "invalid"

    @classmethod
    def get_result_from_whitelist(
        cls, content: str, target: query_target
    ) -> str | None:
        whitelist_dir: str | None = None
        if server_dir:
            whitelist_dir = os.path.join(server_dir, "whitelist.json")
        if not whitelist_dir:
            return None
        if os.path.exists(whitelist_dir):
            with open(whitelist_dir, "r") as f:
                whitelist: dict = json.load(f)
            if target == "player":
                for i in whitelist:
                    if i.get("uuid", None) == content:
                        return i.get("name", None)
                return None
            else:
                for i in whitelist:
                    if i.get("name", None) == content:
                        return i.get("uuid", None)
                return None
        return None

    @classmethod
    def get_result_from_usercache(
        cls, content: str, target: query_target
    ) -> str | None:
        usercache_dir: str | None = None
        if server_dir:
            usercache_dir = os.path.join(server_dir, "usercache.json")
        if not usercache_dir:
            return None
        if os.path.exists(usercache_dir):
            with open(usercache_dir, "r") as f:
                usercache: dict = json.load(f)
            if target == "player":
                for i in usercache:
                    if i.get("uuid", None) == content:
                        return i.get("name", None)
                return None
            else:
                for i in usercache:
                    if i.get("name", None) == content:
                        return i.get("uuid", None)
                return None
        return None

    @classmethod
    def get_uuid(cls, name: str) -> str | None:
        result = cls.get_result_from_whitelist(name, "uuid")
        if result:
            return result
        else:
            result = cls.get_result_from_usercache(name, "uuid")
            if result:
                return result

    @classmethod
    def get_player(cls, uuid: str) -> str | None:
        result = cls.get_result_from_whitelist(uuid, "player")
        if result:
            return result
        else:
            result = cls.get_result_from_usercache(uuid, "player")
            if result:
                return result


local_api = LocallyQuery()
