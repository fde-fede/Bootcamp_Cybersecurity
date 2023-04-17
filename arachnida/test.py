import argparse
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
​
​
def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
​
​
def download_images(url, depth, base_path, allowed_extensions):
    
    parsed_url = urlparse(url)
    base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if not img_url:
            continue
        img_url = urljoin(base_url, img_url)
        _, ext = os.path.splitext(img_url)
        if ext.lower() not in allowed_extensions:
            continue
        img_path = os.path.join(base_path, os.path.basename(img_url))
        download_image(img_url, img_path)
    if depth > 0:
        for link in soup.find_all('a'):
            href = link.get('href')
            if not href:
                continue
            href = urljoin(base_url, href)
            if href.startswith(base_url):
                download_images(href, depth - 1, base_path, allowed_extensions)
​
​
def main():
    parser = argparse.ArgumentParser(description='Spider program to extract images from a website')
    parser.add_argument('-r', action='store_true', help='recursively download images')
    parser.add_argument('-l', nargs="?", const = 1, type=int, help='maximum recursion depth')
    parser.add_argument('-p', default='./data/', nargs="?", const='./data/', help='download path')
    parser.add_argument('url', nargs="?", help='URL to extract images from')
    args = parser.parse_args()
    if str.startswith(args.p, "http"):
        args.url = args.p
        args.p = "./data/"
​
    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
​
    if not os.path.exists(args.p):
        os.makedirs(args.p)
​
    download_images(args.url, args.l, args.p, allowed_extensions)
​
    if args.r:
        print(f'Downloading recursively with depth {args.l}')
    else:
        print('Downloading non-recursively')
​
​
if __name__ == '__main__':
    main()