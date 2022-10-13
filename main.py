import base64

from deta import Base, Drive
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from models import Image

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])
pages = Jinja2Templates(directory="static")
cdn = Base("images")
images = Drive("images")


# class ContentResponse(Response):
#     def __init__(self, path: str, **kwargs):
#         with open(path, "rb") as f:
#             content = f.read()
#             super().__init__(content=content, **kwargs)


class NoCacheFileResponse(FileResponse):
    def __init__(self, path: str, **kwargs):
        super().__init__(path, **kwargs)
        self.headers["Cache-Control"] = "no-cache"


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    items = await image_all()
    return pages.TemplateResponse("dashboard.html", {"request": request, "items": items["data"]})


# to deliver static files without caching
# (Done by jnsougata... smh -- LemonPi314)
@app.get("/assets/{name}")
async def assets(name: str):
    return NoCacheFileResponse(f"./assets/{name}")


@app.get("/scripts/{name}")
async def scripts(name: str):
    return NoCacheFileResponse(f"./scripts/{name}")


@app.get("/styles/{name}")
async def styles(name: str):
    return NoCacheFileResponse(f"./styles/{name}")


@app.get("/image", response_class=HTMLResponse)
async def image_upload_page(request: Request):
    return pages.TemplateResponse("upload.html", {"request": request})


@app.get("/all")
async def image_all():
    res = cdn.fetch()
    items = res.items
    while res.last:
        res = cdn.fetch(last=res.last)
        items += res.items

    # Better to just return `items`. -- LemonPi314
    return {"data": items}


@app.patch("/update")
async def image_update(id: str, embed_title: str, embed_colour_hex: str):
    cdn.update({"embed": [{"title": embed_title, "colour": embed_colour_hex}]}, key=id)
    return {"id": id}


@app.post("/upload")
async def image_upload(request: Request, image: Image):
    extension = image.filename.split(".")[-1]
    image_data = image.content.split(",")[1].encode("utf-8")
    item = cdn.put(
        {
            "ext": extension,
            # Why non-US spelling? Might come as a suprise to users of the API.
            # Just the way it is, not trying to say US is superior. -- LemonPi314
            "embed": [{"title": None, "colour": None}],
        },
    )
    id = item["key"]
    images.put(f"{id}.{extension}", base64.b64decode(image_data))
    url = f"{request.url.scheme}://{request.url.hostname}/cdn/{id}.{extension}"
    return {"image": url, "id": id}


@app.delete("/delete")
async def image_delete(id: str):
    data = cdn.get(id)
    images.delete(f"{data['key']}.{data['ext']}")
    cdn.delete(id)
    return {"id": id}


@app.get("/info/{id}", response_class=HTMLResponse)
async def image_info(request: Request, id: str):
    info = cdn.get(id)
    return pages.TemplateResponse(
        "info.html",
        {"request": request, "data": info},
    )


@app.get("/cdn/{image}")
async def image_cdn(image: str):
    img = images.get(image)
    return Response(
        img.read(),
        media_type=f"image/{image.split('.')[1]}",
    )


@app.get("/embed/{image}")
async def image_cdn_embed(request: Request, image: str):
    embed = cdn.get(image.split(".")[0])
    return HTMLResponse(
        f"""
        <meta name="twitter:card" content="summary_large_image">
        <meta property="og:title" content="{embed["embed"][0]["title"]}"/>
        <meta property="og:type" content="website"/>
        <meta property="og:image" content="{request.url.scheme}://{request.url.hostname}/cdn/{image}"/>
        <meta name="theme-color" content="{embed["embed"][0]["colour"]}">
        <img alt="image" src="{request.url.scheme}://{request.url.hostname}/cdn/{image}">
        """
    )
