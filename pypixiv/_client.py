import asyncio as _asyncio
import logging as _logging
import typing as _typing

import httpx as _httpx

from . import _models
from . import _responses
from . import _exceptions


class _DEFAULTS:
    SCHEME: _typing.Final[str] = "https"
    BASE_URL: _typing.Final[str] = "pixiv.net"
    USER_AGENT: _typing.Final[str] = \
        "Mozilla/5.0 " \
        "(Windows NT 10.0; Win64; x64) " \
        "AppleWebKit/537.36 (KHTML, like Gecko) " \
        "Chrome/97.0.4692.71 " \
        "Safari/537.36"


class Client:

    def __init__(self, *, scheme: _typing.Literal["http", "https"] = None, base_url: str = None, user_agent: str = None,
                 client: _httpx.AsyncClient = None) -> None:
        """
        init function \n
        :parameter scheme: if not provided, use _Defaults.SCHEME [ https ]
        :parameter base_url: if not provided, use _Defaults.BASE_URL [ pixiv.net ]
        :parameter user_agent: if not provided, use _Defaults.USER_AGENT [ ... ]
        :parameter client: if not provided, use httpx.AsyncClient(), if provided, ignore scheme, base_url, user_agent
        :return None
        :rtype None
        :raise ValueError: if scheme is not in http nor https
        """
        if not scheme:
            scheme = _DEFAULTS.SCHEME
        else:
            if scheme.lower() not in ("http", "https"):
                raise ValueError("scheme must be http or https")
        if not base_url:
            base_url = _DEFAULTS.BASE_URL
        self.client = _httpx.AsyncClient(
            base_url=f"{scheme}://{base_url}",
            headers={
                "referer": f"{scheme}://{base_url}/",
                "user-agent": user_agent if user_agent else _DEFAULTS.USER_AGENT,
            },
            http2=True,
            follow_redirects=True,
        ) if not client else client

    async def get_artwork_images(self, artwork_id: str, *, lang: str = None) -> tuple[_models.ArtworkImage]:
        """
        get artwork images \n
        :parameter artwork_id: artwork id
        :parameter lang: language / ex : ko
        :return: tuple of models.ArtworkImage
        :rtype: tuple[models.ArtworkImage]
        :exception ArtworkNotFound: if artwork is not exists or deleted or tried get r18 artwork while not logged in
        """
        pages: _responses.ArtworkPages = _responses.ArtworkPages(**(await self.client.get(
            url=f"ajax/illust/{artwork_id}/pages{f'?lang={lang}' if lang else ''}",
        )).json())
        if pages.error:
            raise _exceptions.ArtworkNotFound(
                f"an error occurred while retrieve artwork information : {pages.message}"
            )
        return tuple(
            _models.ArtworkImage(
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
        :parameter url: pixiv image url
        :return: an image
        :rtype: bytes
        :exception httpx.HTTPError: if an error occurred while loading image
        :exception InternalError: when unexpected status code returned
        """
        response: _httpx.Response = await self.client.get(url=url)
        match response.status_code:
            case 200:
                return response.content
            case 403:
                raise _httpx.HTTPError(
                    f"an error occurred while retrieve image : 403 Forbidden : {response.text}"
                )
            case 404:
                raise _httpx.HTTPError(
                    f"an error occurred while retrieve image : 404 Not Found : {response.text}"
                )
            case default:
                raise _exceptions.InternalError(
                    f"I00: unexpected status code : {default} : {response.text}\nplease report this to developer"
                )

    async def login(self, identifier: str, password: str) -> None:
        """
        login pixiv \n
        :parameter identifier: pixiv id
        :parameter password: pixiv password
        :return: None
        :rtype: None
        :raise NotImplementedError
        """
        raise NotImplementedError("login is not implemented yet")

    async def search_tag(self, tag: str, *, lang: str = None) -> _models.Tag:
        """
        search tag information \n
        :parameter tag: tag
        :parameter lang: language / ex : ko
        :return: models.Tag
        :rtype: models.Tag
        """
        response: _responses.Tag = _responses.Tag(
            **(await self.client.get(
                url=f"ajax/search/tags/{tag}{f'?lang={lang}' if lang else ''}",
            )).json()
        )
        return _models.Tag(
            tag=response.body.tag,
            word=response.body.word,
            tag_translation=response.body.tagTranslation[response.body.tag] if response.body.tagTranslation else {},
            pixpedia=_models.Pixpedia(
                id=response.body.pixpedia.id,
                description=response.body.pixpedia.abstract,
                image=response.body.pixpedia.image,
                parent=response.body.pixpedia.parentTag,
                children=response.body.pixpedia.childrenTags,
                siblings=response.body.pixpedia.siblingsTags,
                yomigana=response.body.pixpedia.yomigana,
            )
        )

    async def search(self, query: str, *,
                     exclude_tag: list[str] = None,
                     tag_match: _typing.Literal["partial", "exact"] = "partial",
                     min_height: int = None,
                     max_height: int = None,
                     min_width: int = None,
                     max_width: int = None,
                     tool: _typing.Literal["3D-Coat", "4thPaint", "Acrylic paint", "AfterEffects", "Airbrush",
                                           "AnimationMaster", "ArtRage", "Aseprite", "AzDrawing", "AzDrawing2",
                                           "AzPainter3", "Ballpoint pen", "Blender", "Brush", "Bryce", "CARRARA",
                                           "CINEMA4D", "CLIP STUDIO PAINT", "COMICWORKS", "Calligraphy pen",
                                           "Color ink", "Colored pencil", "Comi Po!", "ComiLabo", "ComicStudio",
                                           "Copic marker", "Coupy pencil", "Crayon", "DAZ Studio", "Dip pen",
                                           "EDGE", "Expression", "Felt-tip pen", "FireAlpaca", "Fireworks",
                                           "Fountain pen", "GIMP", "Gansai", "GraphicsGale", "Hexagon King",
                                           "IllustStudio", "Illustrator", "Inkscape", "Krita", "Lightwave3D",
                                           "Live2D", "MS_Paint", "Maya", "Mechanical pencil", "MediBang Paint",
                                           "Metasequoia", "NekoPaint", "Oekaki Chat", "Oil paint", "Paint", "Paint 3D",
                                           "PaintShopPro", "Painter", "Paintgraphic", "Pastel Crayons", "Pastels",
                                           "Pencil", "PhotoStudio", "Photoshop", "PictBear", "PicturePublisher",
                                           "Pixelmator", "Pixia", "Poser", "Processing", "Procreate", "RETAS STUDIO",
                                           "SAI", "STRATA", "Sculptris", "Shade", "SketchBookPro", "SketchUp",
                                           "Sunny3D", "Tegaki Blog", "Thin maker", "VRoid Studio", "VistaPro",
                                           "Vue", "Watercolor brush", "Watercolors", "XSI", "ZBrush", "dotpict",
                                           "drawr", "e-mote", "ibisPaint", "kokuban.in", "magic marker", "mdiapp",
                                           "modo", "openCanvas", "pixiv Sketch"]):
        pass

    # special methods

    def __del__(self) -> None:
        """
        close AsyncClient automatically \n
        :return: None
        :rtype: None
        """
        try:
            loop = _asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.client.aclose())
            else:
                loop.run_until_complete(self.client.aclose())
        except Exception as e:
            _logging.warning(f"failed to close AsyncClient automatically due to {e}:{type(e).__name__}")

    async def __aenter__(self) -> 'Client':
        """
        asynchronous context manager enter method \n
        :return: Client
        :rtype: Client
        """
        return self

    async def __aexit__(self, exception_type: _typing.Union[None, type],
                        exception_value: _typing.Union[None, Exception],
                        exception_traceback: _typing.Union[None, _typing.Any]) -> None:
        """
        asynchronous context manager exit method \n
        :parameter exception_type: exception type
        :parameter exception_value: exception class
        :parameter exception_traceback: exception traceback class
        :return: None
        :rtype: None
        """
        await self.client.aclose()
        return None
