import requests
from typing import List
from pathlib import Path

def download_to_local(url:str, out_path:Path, parent_mkdir:bool=True) -> bool:
    if not isinstance(out_path, Path):
        raise ValueError(f'{out_path} must be a valid pathlib.Path object')
    if parent_mkdir:
        out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        filename = url.split('/')[-1]
        file_path = out_path / filename
        response = requests.get(url)
        response.raise_for_status()
        out_path.write_bytes(response.content)
        print(f'Downloaded {filename} to {file_path}')
        return True
    except requests.RequestException as e:
        print(f'Failed to download {url}: {e}')
        return False