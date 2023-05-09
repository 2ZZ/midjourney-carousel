#!/usr/bin/env python3

import json
from bs4 import BeautifulSoup
import requests
import sys

url = "https://www.midjourney.com/showcase/recent/"
template_path = 'midjourney.html.tpl'
output_path = 'midjourney.html'


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


def get_carousel_items(json_data):
    items = []
    jobs = json_data.get('props', {}).get('pageProps', {}).get('jobs', [])
    active = "active"
    for job in jobs:
        image_paths = job.get('image_paths', [])
        if image_paths:
            items.append(
                f'<div class="carousel-item d-flex justify-content-center vh-100 {active}" data-bs-interval="4000">' +
                f'<img class="d-block vh-100" src="{image_paths[0]}"/>' +
                '</div>')
        if active:
            active = ""
    return items


def generate_html(carousel_items):
    # Read the template file
    with open(template_path, 'r') as template_file:
        template_html = template_file.read()

    # Insert the div content into the template
    generated_html = template_html.replace(
        '{{ carousel_items }}', "\n".join(carousel_items))

    # Write the generated HTML to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(generated_html)


def main():
    json_data = get_json_data(url)

    if not json_data:
        print("No JSON data found.")
        sys.exit(1)

    carousel_items = get_carousel_items(json_data)

    generate_html(carousel_items)


if __name__ == "__main__":
    main()
