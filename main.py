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
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")


@app.get("/")
async def home(request: fastapi.Request):
    return pages.TemplateResponse("home.html", {"request": request})


@app.get("/dashboard")
async def dashboard(request: fastapi.Request):
    res = cdn.fetch()
    all_items = res.items

    while res.last:
        res = cdn.fetch(last=res.last)
        all_items += res.items

    return pages.TemplateResponse(
        "dashboard.html",
        {"request": request, "items": all_items},
    )


@app.get("/image")
async def image_upload_page(request: fastapi.Request):
    return pages.TemplateResponse("upload.html", {"request": request})


@app.get("/all")
def image_all():
    res = cdn.fetch()
    all_items = res.items

    while res.last:
        res = cdn.fetch(last=res.last)
        all_items += res.items

    return {"data": all_items}


@app.patch("/state")
def image_state(id: str, visibility: bool):
    cdn.update({"visibility": visibility}, id)
    return {"id": id, "visibility": visibility}


@app.post("/upload")
def upload_image(
    request: fastapi.Request,
    embed_title: str = None,
    embed_colour_hex: str = None,
    image: fastapi.UploadFile = fastapi.File(...),
):
    name = cdn.put(
        {
            "visibility": False,
            "ext": image.filename.split(".")[1],
            "embed": [{"title": embed_title, "colour": embed_colour_hex}],
        }
    )
    images.put(f"{name['key']}.{image.filename.split('.')[1]}", image.file)
    return {
        "image": f"{request.url.scheme}://{request.url.hostname}/{name['key']}.{image.filename.split('.')[1]}",
        "id": name["key"],
    }


@app.delete("/delete")
def delete_image(id: str):
    data = cdn.get(id)
    images.delete(f"{data['key']}.{data['ext']}")
    cdn.delete(id)
    return {"id": id}


@app.get("/info/{id}")
def image_info(request: fastapi.Request, id: str):
    info = cdn.get(id)
    return pages.TemplateResponse(
        "info.html",
        {"request": request, "data": info},
    )


@app.get("/cdn/{image}")
def image_cdn(image: str):
    img = images.get(image)
    return fastapi.responses.StreamingResponse(
        img.iter_chunks(), media_type=f"image/{image.split('.')[1]}"
    )


@app.get("/embed/{image}")
def image_cdn_embed(request: fastapi.Request, image: str):
    embed = cdn.get(image.split(".")[0])
    return fastapi.responses.HTMLResponse(
        f"""
        <meta name="twitter:card" content="summary_large_image">
        <meta property="og:title" content="{embed["embed"][0]["title"]}"/>
        <meta property="og:type" content="website"/>
        <meta property="og:image" content="{request.url.scheme}://{request.url.hostname}/cdn/{image}"/>
        <meta name="theme-color" content="{embed["embed"][0]["colour"]}">
        <img alt="image" src="{request.url.scheme}://{request.url.hostname}/cdn/{image}">
        """
    )
