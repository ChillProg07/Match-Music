import random
from urllib.parse import quote_plus

import httpx


ITUNES_SEARCH_URL = "https://itunes.apple.com/search"


VIBE_SEARCH_QUERIES = {
    "cozy": [
        "indie chill",
        "soft acoustic",
        "dream pop",
        "coffeehouse music",
        "lofi chill",
    ],
    "summer": [
        "summer pop",
        "tropical pop",
        "feel good indie",
        "beach chill",
        "sunny dance pop",
    ],
    "romantic": [
        "romantic indie",
        "dream pop love",
        "soft love song",
        "slow pop",
        "romantic acoustic",
    ],
    "night": [
        "night drive",
        "dark pop",
        "synthwave",
        "alternative r&b",
        "moody indie",
    ],
    "mysterious": [
        "dark alternative",
        "ethereal pop",
        "moody electronic",
        "cinematic dark",
        "experimental pop",
    ],
    "dreamy": [
        "dream pop",
        "ethereal indie",
        "ambient pop",
        "shoegaze",
        "soft electronic",
    ],
    "confident": [
        "power pop",
        "confident dance pop",
        "hip hop energy",
        "bold r&b",
        "pop anthem",
    ],
    "sad": [
        "sad indie",
        "melancholic acoustic",
        "slow alternative",
        "emotional pop",
        "sad piano",
    ],
    "party": [
        "dance pop",
        "club hits",
        "electronic party",
        "pop remix",
        "festival dance",
    ],
    "luxury": [
        "smooth r&b",
        "elegant pop",
        "deep house",
        "sophisticated jazz pop",
        "luxury lounge",
    ],
}


async def fetch_tracks_for_query(
    client: httpx.AsyncClient,
    query: str,
    limit: int = 20,
) -> list[dict]:
    params = {
        "term": query,
        "media": "music",
        "entity": "song",
        "limit": limit,
    }

    response = await client.get(
        ITUNES_SEARCH_URL,
        params=params,
    )

    response.raise_for_status()

    return response.json().get("results", [])


async def search_music(
    vibes: list[str],
    limit: int = 5,
) -> list[dict]:
    queries = []

    for vibe in vibes:
        vibe_queries = VIBE_SEARCH_QUERIES.get(
            vibe,
            [f"{vibe} music"],
        )

        queries.extend(vibe_queries)

    random.shuffle(queries)

    selected_queries = queries[:4]

    candidates = []

    async with httpx.AsyncClient(timeout=15.0) as client:
        for query in selected_queries:
            results = await fetch_tracks_for_query(
                client=client,
                query=query,
                limit=15,
            )

            candidates.extend(results)

    random.shuffle(candidates)

    tracks = []
    seen_tracks = set()
    used_artists = set()

    for item in candidates:
        artist = item.get("artistName")
        title = item.get("trackName")

        if not artist or not title:
            continue

        track_key = (
            artist.strip().lower(),
            title.strip().lower(),
        )

        artist_key = artist.strip().lower()

        if track_key in seen_tracks:
            continue

        if artist_key in used_artists:
            continue

        seen_tracks.add(track_key)
        used_artists.add(artist_key)

        youtube_query = quote_plus(
            f"{artist} {title} official audio"
        )

        tracks.append(
            {
                "title": title,
                "artist": artist,
                "album": item.get("collectionName"),
                "genre": item.get("primaryGenreName"),
                "cover_url": item.get("artworkUrl100"),
                "preview_url": item.get("previewUrl"),
                "itunes_url": item.get("trackViewUrl"),
                "youtube_url": (
                    "https://www.youtube.com/results"
                    f"?search_query={youtube_query}"
                ),
            }
        )

        if len(tracks) == limit:
            break

    return tracks