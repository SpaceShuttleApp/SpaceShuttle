import uvicorn
import fastapi
from deta import Drive
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# files = Drive("images")
app = fastapi.FastAPI()
pages = Jinja2Templates(directory="static")
app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get("/")
async def home(request: fastapi.Request):
    return pages.TemplateResponse("home.html", {"request": request})


@app.get("/dashboard")
async def dashboard(request: fastapi.Request):
    return {"Hello, World!"}


''' 
@app.post("/upload")
def upload_file(
    request: fastapi.Request,
    file: fastapi.UploadFile = fastapi.File(...),
):
    name = files.put(file.filename.replace(" ", "_"), file.file)
    return {
        "file": f"{request.url.scheme}://{request.url.hostname}/{name}",
    }


@app.get("/{name}")
def cdn(name: str):
    img = files.get(name)
    ext = name.split(".")[1]
    return fastapi.responses.StreamingResponse(
        img.iter_chunks(), media_type=f"image/{ext}"
    )


@app.get("/embed/{name}")
def cdn_embed(request: fastapi.Request, name: str):
    return fastapi.responses.HTMLResponse(
        f"""
        <meta name="twitter:card" content="summary_large_image">
        <meta property="og:title" content="{name}"/>
        <meta property="og:type" content="website"/>
        <meta property="og:image" content="{request.url.scheme}://{request.url.hostname}/{name}"/>
        <meta property="og:url" content="{request.url.scheme}://{request.url.hostname}/"/>
        <meta name="url" content="{request.url.scheme}://{request.url.hostname}/">
        <meta name="theme-color" content="#9ECFC2">
        <img alt="image" src="{request.url.scheme}://{request.url.hostname}/{name}">
        """
    )
'''

if __name__ == "__main__":
    uvicorn.run(app)
