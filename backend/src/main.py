from fastapi import FastAPI

app = FastAPI(title="GymApp")

@app.get("/healthz")
def healthz():
	return {"ok": True}

@app.get("/")
def root():
	return {"message": "Hello from FastAPI"}

