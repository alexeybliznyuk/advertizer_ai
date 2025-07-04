from controller.controller import app
from settings.config import settings

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.SENDER_SERVICE_PORT) 