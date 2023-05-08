from pydantic import BaseModel, Field
from typing import Optional

# Creamos la clase/esquema que va a contener tod la info de cada película
class Movie(BaseModel):
    # id: int | None = None ## None es para indicar que puede ser opcional, sin embargo hay otra forma: tiping.
    id: Optional[int] = None
    ## Se pueden agregar validaciones importando Field
    tittle: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(..., ge=1, le=10) ## el menor es 1, ge= greater tahn o equal to, y el max es 10, le=less than or equal to. Los puntos suspensivos indican que el campo es obligatorio y no puede ser nulo
    category: str

    ## Agregamos una clase de ejemplo de como deberia estar formado el objeto de cada película.
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "tittle": "Mi película",
                "overview": "Sinopsis de la película",
                "year": 2022,
                "rating": 7.8,
                "category": "Drama"
            }
        }
  