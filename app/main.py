from urllib.parse import quote_plus
from fastapi import FastAPI, File, HTTPException, UploadFile, Request
from app.image_analyzer import analyze_image
from app.music_service import search_music
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="MatchMusic API",
    description="AI-підбір музики за вайбом фотографії",
    version="0.3.0",
)
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

templates = Jinja2Templates(
    directory="app/templates",
)

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )

@app.post("/analyze-image")
async def analyze_uploaded_image(
    image: UploadFile = File(...)
):
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Можна завантажувати лише JPEG, PNG або WEBP",
        )

    image_bytes = await image.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Файл порожній",
        )

    
    vibes = analyze_image(image_bytes)
    top_vibes = [
    item["vibe"]
    for item in vibes
]

    tracks = await search_music(
    vibes=top_vibes,
    limit=5,
)

    main_vibe = vibes[0]["vibe"]

    search_query = f"{main_vibe} aesthetic music"
    encoded_query = quote_plus(search_query)

    youtube_url = (
        "https://www.youtube.com/results"
        f"?search_query={encoded_query}"
    )

    return {
    "filename": image.filename,
    "main_vibe": vibes[0]["vibe"],
    "detected_vibes": vibes,
    "recommended_tracks": tracks,
}