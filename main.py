import base64

from deta import Base, Drive
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, Response

# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import Image

app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(CORSMiddleware, allow_origins=["*"])
pages = Jinja2Templates(directory="templates")
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
    res = cdn.fetch()
    items = res.items
    while res.last:
        res = cdn.fetch(last=res.last)
        items += res.items
    return pages.TemplateResponse(
        "dashboard.html",
        {"request": request, "items": items},
    )


@app.get("/image", response_class=HTMLResponse)
async def image_upload_page(request: Request):
    return pages.TemplateResponse("upload.html", {"request": request})


@app.get("/info/{id}", response_class=HTMLResponse)
async def image_info(request: Request, id: str):
    info = cdn.get(id)
    return pages.TemplateResponse(
        "info.html",
        {"request": request, "data": info},
    )


# For future features
@app.get("/embed/{image}")
async def image_cdn_embed(request: Request, image: str):
    embed = cdn.get(image.split(".")[0])
    return pages.TemplateResponse(
        "embed.html",
        {"request": request, "embed": embed},
    )


# to deliver static files without caching
# (Done by jnsougata... smh -- LemonPi314)
@app.get("/static/{path:path}")
async def static(path: str):
    return NoCacheFileResponse(f"./static/{path}")


@app.patch("/update")
async def image_update(
    id: str,
    embed_title: str = None,
    embed_colour_hex: str = None,
    visibility: bool = None,
):
    cdn.update(
        {
            "visibility": visibility,
            "embed": [{"title": embed_title, "colour": embed_colour_hex}],
        },
        key=id,
    )
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
            # Don't take the ou out of colour --SlumberDemon
            "visibility": False,  # For future features
            "embed": [{"title": None, "colour": None}],  # For future features
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


@app.get("/cdn/{image}")
async def image_cdn(image: str):
    img = images.get(image)
    return Response(
        img.read(),
        media_type=f"image/{image.split('.')[1]}",
    )
