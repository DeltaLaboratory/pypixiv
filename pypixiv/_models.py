import pydantic as _pydantic


class ArtworkImage(_pydantic.BaseModel):
    width: int
    height: int

    original: str
    regular: str
    small: str
    thumb: str


class Pixpedia(_pydantic.BaseModel):
    id: str = ""
    description: str = ""
    image: str = ""
    parent: str = ""
    children: list[str] = []
    siblings: list[str] = []
    yomigana: str = ""


class Tag(_pydantic.BaseModel):
    tag: str
    word: str
    tag_translation: dict[str, str]  # {en: "cat", ko: "고양이", zh: "猫", zh_tw: "貓", romaji: "neko"}
    pixpedia: Pixpedia
