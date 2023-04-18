from bs4 import BeautifulSoup
import argparse
import requests
import os
import shutil
import sys
from urllib.parse import urlparse, urljoin

def download_images(url, depth, base_path, allowed_extensions):
    count = 0
    parsed_url = urlparse(url)
    base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    if base_url.startswith("http"):
        web = 1
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
    else:
        try:
            with open(base_path, 'r') as f:
                web = 0
                r = f.read()
                soup = BeautifulSoup(r, 'html.parser')
        except ValueError:
            print(f"{base_path} does not exist")
    images = soup.find_all('img')
    print(f"Total {len(images)} Image Found!")
    if len(images) != 0:
        for i, image in enumerate(images):
            try:
                image_url = image.get('src')
            except:
                pass
            _, ext = os.path.splitext(image_url)
            if ext.lower() not in allowed_extensions:
                continue
            if web == 0:
                try:
                    with open(base_path, 'a') as f:
                        response = open(image_url, 'rb')
                        shutil.copyfileobj(response, f)
                except:
                    pass
            else:
                image_url = urljoin(base_url, image_url)
                try:
                    r = requests.get(image_url).content
                    try:
                        r = str(r, 'utf-8')
                    except UnicodeDecodeError:
                        print ("A")
                        with open(f"{base_path}/images{i+1}{ext}", "wb+") as f:
                            f.write(r)
                    count += 1
                except:
                    pass
        if depth > 0:
            for link in soup.find_all('a'):
                href = link.get('href')
                if not href:
                    continue
                href = urljoin(base_url, href)
                if href.startswith(base_url):
                    download_images(href, depth - 1, base_path, allowed_extensions)
        if count == len(images):
            print("All Images Downloaded!")
        else:
            print(f"Total {count} Images Downloaded Out of {len(images)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Spider program to extract images from a URL')
    parser.add_argument('-r', action='store_true', help='recursively downloads images from the URL given as parameter')
    parser.add_argument('-l', nargs="?", const=5, type=int, help="indicates the max depth level of recursively download")
    parser.add_argument('-p', default='./data/', help='download path')
    parser.add_argument('url', nargs="?", help='URL to extract images from')
    args = parser.parse_args()
    if str.startswith(args.p, "http"):
        args.url = args.p
        args.p = "./data/"
    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    if not os.path.exists(args.p):
        os.makedirs(args.p)
    download_images(args.url, args.l, args.p, allowed_extensions)
    if args.r:
        print(f'Downloading recusively with depth {args.l}')
    else:
        print('Downloading non-recursively')