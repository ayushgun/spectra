import argparse
import base64
import os

from eyesight import Snapshot, Tourguide

Snapshot.gc_project_id = "spectra-405610"
Snapshot.gc_service_key_file = "../keys/service_account_caption.json"
guide = Tourguide("../keys/palm_key.json")


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
    os.system(f"kitten icat {args.file_path}")
    snapshot = Snapshot(b64)

    if snapshot.has_hazard():
        print(guide.generate_contextual_description(snapshot))
    else:
        print("No harmful objects detected")


if __name__ == "__main__":
    main()
