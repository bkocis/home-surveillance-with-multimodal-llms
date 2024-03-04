import cv2
import ollama
import sys
import datetime


def query_the_image(query: str, image_list: list[str]) -> ollama.chat:
    try:
        res = ollama.chat(
            model='llava:7b-v1.6-mistral-q2_K',
            messages=[
                {
                    'role': 'user',
                    'content': query,
                    'images': image_list,
                }
            ]
        )
    except Exception as e:
        print(f"Error: {e}")
        return None
    return res['message']['content']


def observe_scene_change(initial_scene: str, image):
    queries = [f"You are a home surveillance system - "
               f"you need to observe the image and report very short way with only yes or no "
               f"if you see something different in the image relative to the initial scene described as "
               f"'{initial_scene}'. "
               f"Don't use any other sentences to describe the image!",
               "report very short way with only yes or no - Do you see people in the image?",
               "report very short way with only yes or no - Do you see someone steeling something?",
               "report very short way with only yes or no - Do you see people moving?"
               ]
    for guery in queries:
        print_out_the_response(guery, image_list=image)


def print_out_the_response(query_message: str, image_list: list[str]) -> None:
    response = query_the_image(query_message, image_list)
    if response:
        print(f"{str(datetime.datetime.now())}, {response}")
        sys.stdout.flush()
        sys.stdout.write("\n")
    return response


def display_image(cap: cv2.VideoCapture):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Webcam Live', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def image_processing_function(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Webcam Live', gray)
    image = [cv2.imencode('.jpg', gray)[1].tobytes()]
    # scene_description = print_out_the_response("what is on the image?", image_list=image)
    # observe_scene_change(initial_scene=initial_scene, image=image)
    print_out_the_response("Is there something dangerous going on in the image? Answer with yes or no!",
                           image_list=image)


def frame_generator(cap: cv2.VideoCapture):
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_number += 1
        yield frame_number, frame


def display_frame_generator(cap: cv2.VideoCapture, image_processing_function: callable, every_nth_second: int):
    frame_rate = 30
    for frame_number, frame in frame_generator(cap):
        if frame_number % (every_nth_second * frame_rate) == 0:
            image_processing_function(frame)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # display_image(cap)  # for visual debugging

    display_frame_generator(cap, image_processing_function=image_processing_function, every_nth_second=5)


"""
import concurrent.futures

def process_frame(frame):
    return cv2.imencode('.jpg', frame)[1].tobytes()

with concurrent.futures.ThreadPoolExecutor() as executor:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        future = executor.submit(process_frame, frame)
        image = future.result()
"""