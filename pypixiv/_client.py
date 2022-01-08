import typing as _typing

import httpx as _httpx

from . import _models
from . import _responses
from . import _exceptions


class _Defaults:
    SCHEME: _typing.Final[str] = "https"
    BASE_URL: _typing.Final[str] = "pixiv.net"
    USER_AGENT: _typing.Final[str] = \
        "Mozilla/5.0 " \
        "(Windows NT 10.0; Win64; x64) " \
        "AppleWebKit/537.36 (KHTML, like Gecko) " \
        "Chrome/97.0.4692.71 " \
        "Safari/537.36"


class Client:

    def __init__(self, *, scheme: str = None, base_url: str = None, user_agent: str = None) -> None:
        """
        init function \n
        :parameter scheme: if not provided, use _Defaults.SCHEME [ https ]
        :parameter base_url: if not provided, use _Defaults.BASE_URL [ pixiv.net ]
        :parameter user_agent: if not provided, use _Defaults.USER_AGENT [ ... ]
        :return None
        :rtype None
        :raise ValueError: if scheme is not in http nor https
        """
        if not scheme:
            scheme = _Defaults.SCHEME
        else:
            if scheme.lower() not in ("http", "https"):
                raise ValueError("scheme must be http or https")
        if not base_url:
            base_url = _Defaults.BASE_URL
        self.client = _httpx.AsyncClient(
            base_url=f"{scheme}://{base_url}",
            headers={
                "referer": f"{scheme}://{base_url}/",
                "user-agent": user_agent if user_agent else _Defaults.USER_AGENT,
            }
        )

    async def get_artwork(self, artwork_id: int, *, lang: str = None) -> tuple[_models.Image]:
        """
        get artwork images \n
        :parameter artwork_id: artwork id
        :parameter lang: language / ex : ko
        :return: tuple of models.Image
        :rtype: tuple[_models.Image]
        :exception ArtworkNotFound: if artwork is not exists or deleted
        """
        pages: _responses.ArtworkPages = _responses.ArtworkPages(**(await self.client.get(
            url=f"ajax/illust/{artwork_id}/pages{f'?lang={lang}' if lang else ''}"
        )).json())
        if pages.error:
            raise _exceptions.ArtworkNotFound(
                f"an error occurred while retrieve artwork information : {pages.message}"
            )
        return tuple(
            _models.Image(
                thumb=page.urls.thumb_mini,
                small=page.urls.small,
                regular=page.urls.regular,
                original=page.urls.original,
                width=page.width,
                height=page.height
            ) for page in pages.body
        )

    async def get_image(self, url: str) -> bytes:
        """
        get an image - you should load image with this method \n
        :param url: an url provided at get_artwork
        :return: an image
        :rtype: bytes
        """
        return (await self.client.get(url)).content
