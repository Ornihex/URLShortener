from fastapi import FastAPI, status
from routes.shorten import router
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

app.include_router(router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)