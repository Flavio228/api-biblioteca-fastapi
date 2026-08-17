from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class LibroCrear (BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    anio: int = Field(gt=0, le=date.today().year)

class LibroRespuesta (BaseModel):
    id: int
    titulo: str
    autor: str
    anio: int
    leido: bool
