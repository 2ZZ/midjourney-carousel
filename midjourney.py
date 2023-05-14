#!/usr/bin/env python3

import json
from bs4 import BeautifulSoup
import requests
import sys

url = "https://www.midjourney.com/showcase/recent/"
output_path = 'public/images.json'


def get_json_data(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: Unable to fetch URL ({response.status_code})")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find(
        'script', {'id': '__NEXT_DATA__', 'type': 'application/json'})

    if script_tag:
        json_data = json.loads(script_tag.string)
        return json_data
    else:
        print("No script tag with specified attributes found.")
        return None


def get_carousel_images(json_data):
    items = []
    jobs = json_data.get('props', {}).get('pageProps', {}).get('jobs', [])
    for job in jobs:
        image_paths = job.get('image_paths', [])
        if image_paths:
            items.append(image_paths[0])
    return items


def save_to_json(carousel_images):
    print(f"Saving images to {output_path}")
    with open(output_path, 'w') as f:
        f.write(json.dumps(carousel_images, indent=2))


def main():
    json_data = get_json_data(url)

    if not json_data:
        print("Error: No JSON data found.")
        sys.exit(1)

    carousel_images = get_carousel_images(json_data)

    save_to_json(carousel_images)


if __name__ == "__main__":
    main()
