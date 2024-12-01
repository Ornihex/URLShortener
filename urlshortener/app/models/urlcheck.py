from pydantic import AnyUrl, BaseModel, field_validator

class Url(BaseModel):
    '''
    This model validates the url and converts it to a string data type
    '''
    url: AnyUrl
    @field_validator('url', mode = 'after')
    def set_url(cls, v):
        return str(v)
