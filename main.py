import codecs
import fastapi
from deta import Base, Drive
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response


cdn = Base("images")
images = Drive("images")


class ContentResponse(Response):
    def __init__(self, path: str, **kwargs):
        with open(path, "rb") as f:
            content = f.read()
            super().__init__(content=content, **kwargs)


app = fastapi.FastAPI()
pages = Jinja2Templates(directory="static")
app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get("/")
async def dashboard(request: fastapi.Request):
    res = cdn.fetch()
    all_items = res.items

    while res.last:
        res = cdn.fetch(last=res.last)
        all_items += res.items

    return pages.TemplateResponse(
        "dashboard.html", {"request": request, "items": all_items}
    )


# to deliver static files withouth caching
@app.get("/assets/{name}")
async def file(name: str):
    return ContentResponse(f"./assets/{name}", media_type="application/octet-stream")


@app.get("/scripts/{name}")
async def file(name: str):
    return ContentResponse(f"./scripts/{name}", media_type="text/javascript")


@app.get("/styles/{name}")
async def file(name: str):
    return ContentResponse(f"./styles/{name}", media_type="text/css")


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


@app.patch("/update")
def image_update(id: str, embed_title: str, embed_colour_hex: str):
    cdn.update({"embed": [{"title": embed_title, "colour": embed_colour_hex}]}, id)
    return {"id": id}


@app.post("/upload")
async def upload_image(request: fastapi.Request):
    data = await request.json()
    filename = data["filename"]
    extension = filename.split(".")[-1]
    image_data = data["content"].split(",")[1].encode("utf-8")
    name = cdn.put(
        {
            "ext": extension,
            "embed": [{"title": None, "colour": None}],
        }
    )
    images.put(f"{name['key']}.{extension}", codecs.decode(image_data, "base64"))
    uri = f"{request.url.scheme}://{request.url.hostname}/cdn/{name['key']}.{extension}"
    return {"image": uri, "id": name["key"]}


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
