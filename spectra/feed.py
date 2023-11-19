import base64
import os
import time
from functools import lru_cache
from multiprocessing import Process, Queue

import cv2

from eyesight import Snapshot, Tourguide
from speech import TTSMessage, VoiceGender

# Set initial configuration variables
Snapshot.gc_project_id = "spectra-405610"
TTSMessage.gc_project_id = "spectra-405610"
Snapshot.gc_service_key_file = "../keys/service_account_caption.json"
TTSMessage.gc_service_key_file = "../keys/service_account_audio.json"

guide = Tourguide("../keys/palm_key.json")
ESC = 27


@lru_cache(maxsize=128)
def get_cached_description(uri: str) -> str:
    image_frame = Snapshot(uri)

    if not image_frame.has_hazard():
        return guide.generate_contextual_description(image_frame)

    return "No harmful objects detected"


def process_frame(image_uri, result_queue):
    description = get_cached_description(image_uri)
    result_queue.put(description)

    if description == "No harmful objects detected":
        return

    tts_message = TTSMessage(description)
    tts_message.to_audio("output.mp3", gender=VoiceGender.FEMALE)
    os.system("afplay output.mp3")


def start_webcam_feed():
    webcam = cv2.VideoCapture(1)
    last_processed_time = time.time()
    result_queue = Queue()
    current_process = None

    while True:
        successful_read, current_frame = webcam.read()
        if not successful_read:
            break

        cv2.imshow("Spectra Mobile", current_frame)

        if time.time() - last_processed_time >= 15:
            if current_process is None or not current_process.is_alive():
                success, encoded_image = cv2.imencode(".jpg", current_frame)
                if not success:
                    raise IOError("Unable to encode current webcam frame")

                base64_encoded_image = base64.b64encode(encoded_image).decode()
                image_uri = f"data:image/jpeg;base64,{base64_encoded_image}"

                current_process = Process(
                    target=process_frame, args=(image_uri, result_queue)
                )
                current_process.start()
                last_processed_time = time.time()

        if not result_queue.empty():
            description = result_queue.get()
            print(description)

        if cv2.waitKey(1) == ESC:
            if current_process is not None:
                current_process.join()
            break

    webcam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_webcam_feed()
