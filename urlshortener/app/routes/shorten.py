from fastapi import APIRouter, Response, status
from fastapi.responses import RedirectResponse
import random
from mongoAPI import MongoDB
from pprint import pprint
from models.urlcheck import Url

router = APIRouter()
db = MongoDB(db_name = 'data', collection = 'shortCodes')

chars = 'abcdefghijklmnopqrstuvwxyz1234567890'


@router.post('/shorten')
async def shorten(url: Url, response: Response):
    data = 0
    while data == 0:
        shortCode = ''.join(random.choices(chars, k = 6))
        data = db.add_shortCode(url.url, shortCode)
    print(shortCode)
    data.pop('_id')
    data.pop('accessCount')
    response.status_code = status.HTTP_201_CREATED
    return data



@router.get('/shorten/{shortCode}/stats')
async def get_stats(shortCode: str, response: Response):
    try:
        data = db.get_stats(shortCode)
        data.pop('_id')
        print(data)
        response.status_code = status.HTTP_200_OK
        return data
    except:
        response.status_code = status.HTTP_404_NOT_FOUND

@router.get('/shorten/{shortCode}')
async def retrieve_original_url(shortCode: str, response: Response):
    try:
        data = db.get_url(shortCode)
        data.pop('_id')
        data.pop('accessCount')
        response.status_code = status.HTTP_200_OK
        print(data)
        return data
    except:
        response.status_code = status.HTTP_404_NOT_FOUND

@router.put('/shorten/{shortCode}')
async def update_short(shortCode: str, url: Url, response: Response):
    try:
        data = db.update(shortCode, url.url)
        data.pop('_id')
        data.pop('accessCount')
        response.status_code = status.HTTP_200_OK
        print(data)
        return data
    except:
        response.status_code = status.HTTP_404_NOT_FOUND

@router.delete('/shorten/{shortCode}')
async def delete_short(shortCode: str, response: Response):
    try:
        db.delete(shortCode)
        response.status_code = status.HTTP_204_NO_CONTENT
    except:
        response.status_code = status.HTTP_404_NOT_FOUND