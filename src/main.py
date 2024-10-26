#main.py
from fastapi import FastAPI
from routes import router  # Import router from routes

app = FastAPI()

# Include the router from the endpoints
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

