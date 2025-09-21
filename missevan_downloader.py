import time
import os
import re
import sys
from mimetypes import guess_extension

import asyncio
import aiofiles
import validators
from aiohttp import ClientSession

base_url = "https://www.missevan.com"

if getattr(sys, 'frozen', False):
    app_path = os.path.abspath('.')
else:
    app_path = os.path.dirname(__file__)

download_folder = os.path.join(app_path, 'dl')

if not os.path.exists(download_folder):
    os.mkdir(download_folder)

def is_drama_link(url):
    if "drama" in url:
        return True
    return False

invalid_characters = r"^[ .]|[/<>:\"\\|?*]+|[ .]$"
def sanitize_filename(filename):
    """Replaces any invalid characters"""
    return re.sub(invalid_characters, "_", filename) 

async def get_default_headers():
    """Return headers with optional token cookie"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0 Safari/537.36"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://www.missevan.com/",
    }

    # append cookie
    token_path = os.path.join(app_path, 'token.txt')
    if os.path.exists(token_path):
        async with aiofiles.open(token_path, 'r') as f:
            token_value = (await f.read()).strip()
        headers["Cookie"] = f"token={token_value}"

    return headers

async def download_audio(id, session, **kwargs):
    url = f"{base_url}/sound/getsound?soundid={id}"
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()

    json_content = await resp.json()

    sound_title = sanitize_filename(json_content['info']['sound']['soundstr']) 
    sound_url = json_content['info']['sound'].get('soundurl')
    if sound_url is None:
        print(f"Unable to download file for {sound_title}")
        return

    resp = await session.request(method="GET", url=sound_url)
    file_extension = guess_extension(resp.content_type)
    if file_extension is not None:
        file_name = f"{sound_title}{file_extension}"
    else:
        file_name = sound_title

    download_path = os.path.join(download_folder, file_name)
    chunk_size = 1024 * 1024 * 1024 * 4 # 4 GiB
    async with aiofiles.open(download_path, 'wb') as f:
        async for chunk in resp.content.iter_chunked(chunk_size):
            await f.write(chunk)
    print(f"Download finished for {download_path}")

async def fetch_audio_list(drama_id, session, **kwargs):
    url = f"{base_url}/dramaapi/getdrama?drama_id={drama_id}"
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    
    json_content = await resp.json()
    audio_ids = set()
    for episode in json_content['info']['episodes']['episode']:
        if episode['sound_id'] not in audio_ids:
            audio_ids.add(episode['sound_id'])
    return audio_ids

async def main():
    url = input("Please paste the full url here: ")
    if not validators.url(url):
        return
    headers = await get_default_headers()
    async with ClientSession(headers=headers) as session:
        if not is_drama_link(url):
            audio_id = url.split('=')[-1]
            await download_audio(audio_id, session)
        else:
            drama_id = url.split('/')[-1]
            audio_list = await fetch_audio_list(drama_id, session)
            tasks = []
            for audio_id in audio_list:
                tasks.append(
                    download_audio(audio_id, session)
                )
            await asyncio.gather(*tasks)

if __name__ == '__main__':
    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."

    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"Job took {elapsed:.2f} seconds.")