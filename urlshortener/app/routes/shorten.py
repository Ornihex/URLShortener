from fastapi import APIRouter, Response, status
from fastapi.responses import RedirectResponse
import random
from mongoAPI import MongoDB
from pprint import pprint
from models.urlcheck import Url

force_redirect = input('Need to force redirection? Type Y if yes, or skip(press enter) if no: ')
if force_redirect.lower() == 'y':
    force_redirect = True
else:
    force_redirect = False


router = APIRouter()
db = MongoDB(db_name = 'data', collection = 'shortCodes')

chars = 'abcdefghijklmnopqrstuvwxyz1234567890'


@router.post('/shorten')
async def shorten(url: Url, response: Response) -> dict:
    '''
    shorten(url) -> dict

    This function takes a url using a POST method, generates a short code and adds it to the database using the api(see mongoAPI.py).
    Returns the response code 201 Created if successful or 400 Bad Request if url validation failed

    arguments:
    url -- site url. Correct example: https://example.org
                     Wrong example: example.org
    '''
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
async def get_stats(shortCode: str, response: Response) -> dict:
    '''
    This function get statistics for a short URL using the GET method.
    The endpoint returns a 200 OK status code with the statistics or
    404 Not Found if the short URL was not found.

    arguments:
    shortCode: url short code.
    '''
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
    '''
    This function retrieve the original URL from a short URL using the GET method.
    The endpoint return 200 Ok status code with the original url if force redirection is disabled,
    307 Temporary Redirect status code and redirects to original url if force redirection is enabled or
    404 Not Found status code if the short url was not found.

    arguments:
    shortCode -- url short code.
    '''
    try:
        data = db.get_url(shortCode)
        data.pop('_id')
        data.pop('accessCount')
        response.status_code = status.HTTP_200_OK
        print(data)
        if force_redirect:
            return RedirectResponse(data['url'])
        else:
            return data
    except:
        response.status_code = status.HTTP_404_NOT_FOUND

@router.put('/shorten/{shortCode}')
async def update_short(shortCode: str, url: Url, response: Response):
    '''
    This function updates an existing short URL using the PUT method.
    The endpoint validates the request body and returns a 200 OK status code with the updated short URL
    or 400 Bad Request status code if url validation failed
    or 404 Not Found status code if short url was not found.

    arguments:
    shortCode -- url short code.
    url -- site url. Correct example: https://example.org
                     Wrong example: example.org
    '''
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
    '''
    This function deletes an existing short URL using the DELETE method.
    The endpoint returns a 204 No Content status code if the short URL was successfully deleted
    or a 404 Not Found status code if the short URL was not found.

    arguments:
    shortCode -- url short code.
    '''
    try:
        db.delete(shortCode)
        response.status_code = status.HTTP_204_NO_CONTENT
    except:
        response.status_code = status.HTTP_404_NOT_FOUND