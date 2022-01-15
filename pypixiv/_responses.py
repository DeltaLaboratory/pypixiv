import pydantic as _pydantic


class ArtworkPagesUrl(_pydantic.BaseModel):
    thumb_mini: str
    small: str
    regular: str
    original: str


class ArtworkPagesImage(_pydantic.BaseModel):
    urls: ArtworkPagesUrl
    width: int
    height: int


class ArtworkPages(_pydantic.BaseModel):
    error: bool
    message: str
    body: list[ArtworkPagesImage]


class TagBodyBreadCrumbsSuccessor(_pydantic.BaseModel):
    tag: str
    translation: dict[str, str]


class TagBodyBreadCrumbs(_pydantic.BaseModel):
    current: list[str]
    successor: list[TagBodyBreadCrumbsSuccessor]


class TagBodyPixpedia(_pydantic.BaseModel):
    abstract: str = ""
    id: str = ""
    image: str = ""
    parentTag: str = ""
    siblingsTags: list[str] = []
    childrenTags: list[str] = []
    yomigana: str = ""


class TagBody(_pydantic.BaseModel):
    tag: str
    tagTranslation: dict[str, dict[str, str]]
    word: str
    myFavoriteTags: list[str]
    pixpedia: TagBodyPixpedia
    breadcrumbs: TagBodyBreadCrumbs


class Tag(_pydantic.BaseModel):
    error: bool
    body: TagBody
