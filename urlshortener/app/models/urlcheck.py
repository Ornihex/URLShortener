from pydantic import AnyUrl, BaseModel, field_validator

class Url(BaseModel):
    url: AnyUrl
    @field_validator('url', mode = 'after')
    def set_url(cls, v):
        return str(v)
