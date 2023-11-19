import argparse
import base64
from pprint import pprint

import requests

import ai


def image_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Convert image to base64 and send it to a server."
    )
    parser.add_argument("file_path", type=str, help="Path to the image file")
    args = parser.parse_args()

    b64 = image_to_base64(args.file_path)
    res = requests.post("http://127.0.0.1:8000/snapshot/describe", json={"uri": b64})

    if res.status_code == 204:
        pprint("Image deemed safe")
    elif res.status_code == 200:
        pprint(res.json()["response"])


if __name__ == "__main__":
    main()
