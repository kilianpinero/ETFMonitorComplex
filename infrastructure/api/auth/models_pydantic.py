from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr = Field(..., min_length=1, description="Email obligatorio")
    password: str = Field(..., min_length=1, description="Contraseña obligatoria")

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"

class TickerPreferencesCreate(BaseModel):
    ticker: str = Field(..., description="Ticker obligatorio")
    drop_percentage: float = Field(..., description="Porcentaje de caída obligatorio", gt=0, le=100)
    days: int = Field(..., description="Días obligatorio", gt=0, le=365)

class TickerPreferencesUpdate(BaseModel):
    ticker: str | None = None
    drop_percentage: float | None = Field(None, gt=0, le=100)
    days: int | None = Field(None, gt=0, le=365)

class TickerPreferencesOut(BaseModel):
    id: str
    ticker: str
    drop_percentage: float
    days: int
    email: str
    class Config:
        orm_mode = True
