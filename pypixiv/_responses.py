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
