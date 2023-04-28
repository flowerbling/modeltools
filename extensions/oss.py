import os
import re
from typing import IO, List, Tuple, Union
from urllib.parse import quote as urlquote
from urllib.parse import unquote as urlunquote
from urllib.parse import urlparse, urlunparse

import oss2

__all__ = ["Oss"]


class OssExt():
    __oss: oss2.Bucket = None # type: ignore
    __endpoint_name: str = ""
    __endpoint: str = ""
    __public_endpoint: str = ""

    @property
    def name(self):
        return "oss"

    @property
    def bucket(self):
        return self.__oss.bucket_name

    @property
    def endpoint_name(self) -> str:
        return self.__endpoint_name

    def __init__(self):
        access_id = os.environ.get("OssAccessId")
        access_key =os.environ.get("OssAccessKey")
        bucket = os.environ.get("OssOssBucket")

        self.__endpoint_name = os.environ.get("OssEndPointName", "")
        self.__endpoint = os.environ.get("OssEndPoint", "")
        self.__public_endpoint =os.environ.get("OssPublicEndPoint", "")

        self.__oss = oss2.Bucket(
            oss2.Auth(access_key_id=access_id, access_key_secret=access_key),
            self.__endpoint,
            bucket,
        )

        self.list_objects = self.__oss.list_objects_v2
        self.list_object_versions = self.__oss.list_object_versions
        self.delete_object = self.__oss.delete_object
        self.object_exists = self.__oss.object_exists
        self.get_object = self.__oss.get_object
        self.object_exists = self.__oss.object_exists

    def to_oss_url(
        self, path: Union[str, os.PathLike], internal: bool = False, expires: int = 0
    ) -> str:
        if expires:
            oss_url = self.__oss.sign_url("GET", str(path).lstrip("/"), expires)
            if internal:
                return oss_url

            return oss_url.replace(self.__endpoint, self.__public_endpoint)

        return f'https://{self.__oss.bucket_name}.{self.__endpoint if internal  else self.__public_endpoint}/{urlquote(str(path).lstrip("/"))}'

    def to_oss_internal_url(self, oss_public_url: str) -> str:
        scheme, netloc, path, params, query, fragment = urlparse(oss_public_url)
        if scheme not in ["http", "https"]:
            return oss_public_url

        if not netloc.endswith(".aliyuncs.com"):
            return oss_public_url

        if netloc.endswith("-internal.aliyuncs.com"):
            return oss_public_url

        netloc = re.sub(
            r"([a-zA-Z0-9-]+)(\.oss-[a-z-]+)(\.aliyuncs\.com)",
            r"\1\2-internal\3",
            netloc,
        )

        return urlunparse((scheme, netloc, path, params, query, fragment))

    def to_oss_cdn_url(self, oss_public_url: str) -> str:
        _, _, path, params, query, fragment = urlparse(oss_public_url)

        return urlunparse(('https', 'cdn-video.jushuo.tv', path, params, query, fragment))

    def oss_url_to_key(self, path_or_url: str) -> str:
        parts = urlparse(path_or_url)
        if not parts.hostname:
            return ""

        if parts.hostname.endswith(".aliyuncs.com") and parts.hostname.startswith(
            self.__oss.bucket_name + "."
        ):
            path = path_or_url.split(".aliyuncs.com", 1)[1]

            return urlunquote(path).lstrip("/")

        return ""

    def upload_data(
        self, data: Union[bytes, str, IO], dest: Union[str, os.PathLike]
    ) -> str:
        dest = str(dest)

        self.__oss.put_object(dest.lstrip("/"), data)

        return self.to_oss_url(dest)

    def upload_file(
        self, src: Union[str, os.PathLike], dest: Union[str, os.PathLike]
    ) -> str:
        src, dest = str(src), str(dest)

        self.__oss.put_object_from_file(dest.lstrip("/"), src)

        return self.to_oss_url(dest)

    def copy_object(self, src_key: str, dest_key: str):
        return self.__oss.copy_object(self.__oss.bucket_name, src_key, dest_key)

    def batch_delete_object(self, file_keys: List[str]):
        if not file_keys:
            return

        batch_size = 300
        while file_keys:
            self.__oss.batch_delete_objects(file_keys[:batch_size])

            file_keys = file_keys[batch_size:]

    def batch_delete_object_versions(
        self, file_keys_and_versions: List[Tuple[str, str]]
    ):
        if not file_keys_and_versions:
            return

        batch_size = 300
        while file_keys_and_versions:
            self.__oss.delete_object_versions(
                oss2.models.BatchDeleteObjectVersionList(
                    [
                        oss2.models.BatchDeleteObjectVersion(*fkv)
                        for fkv in file_keys_and_versions[:batch_size]
                    ]
                )
            )

            file_keys_and_versions = file_keys_and_versions[batch_size:]


Oss = OssExt()