import pydantic as _pydantic


class Image(_pydantic.BaseModel):
    width: int
    height: int

    original: str
    regular: str
    small: str
    thumb: str
