import uvicorn
import fastapi
from deta import Base, Drive
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

cdn = Base("images")
images = Drive("images")

app = fastapi.FastAPI()
pages = Jinja2Templates(directory="static")
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.mount("/styles", StaticFiles(directory="styles"), name="styles")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


@app.get("/")
async def home(request: fastapi.Request):
    return pages.TemplateResponse("home.html", {"request": request})


@app.get("/dashboard")
async def dashboard(request: fastapi.Request):
    return {"Hello, World!"}


@app.patch("/state")
def image_state(id: str, public: bool):
    cdn.update({"public": public}, id)
    return {"id": id, "state": public}


@app.post("/upload")
def upload_image(
    request: fastapi.Request,
    embed_title: str,
    embed_colour_hex: str,
    image: fastapi.UploadFile = fastapi.File(...),
):
    name = cdn.put(
        {"public": False, "embed": [{"title": embed_title, "colour": embed_colour_hex}]}
    )
    images.put(f"{name['key']}.{image.filename.split('.')[1]}", image.file)
    return {
        "image": f"{request.url.scheme}://{request.url.hostname}/{name['key']}.{image.filename.split('.')[1]}",
        "id": name["key"],
    }


''' 
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
