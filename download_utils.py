import requests

def download_file(url: str, output_path: str):
    r = requests.get(url, allow_redirects=True)
    open(output_path, 'wb').write(r.content)