import cv2
import ollama
import time
import sys
import math


def query_the_image(query: str, image_list: list[str]) -> ollama.chat:
    try:
        res = ollama.chat(
            model='llava:7b-v1.6-mistral-q2_K',
            messages=[
                {
                'role': 'user',
                'content':query,
                'images': image_list,
                }
            ]
        )
    except Exception as e:
        print(f"Error: {e}")
        return None
    return res['message']['content']


# def capture_scene(cap):
#     print("Capturing initial scene description....")
#     ret, frame = cap.read()
#     image = [cv2.imencode('.jpg', frame)[1].tobytes()]
#     response = query_the_image("What do you see on the image", image)
#     print("Capturing initial scene description....done!")
#     return response


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
        print(response)
        sys.stdout.flush()
        sys.stdout.write("\n")


def display_image(cap):
    if not cap.isOpened():
        print("Unable to read camera feed")

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
    initial_scene = print_out_the_response("what is on the image?", image_list=image)
    # observe_scene_change(initial_scene=initial_scene, image=image)


def frame_generator(cap):
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_number += 1
        yield frame_number, frame


def display_frame_generator(cap, image_processing_function):
    for frame_number, frame in frame_generator(cap):
        if frame_number % 30 == 0:
            image_processing_function(frame)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # scene_description = capture_scene(cap)

    # display_image(cap)
    display_frame_generator(cap, image_processing_function=image_processing_function)

    #observe_scene_change(initial_scene=scene_description)



"""
# Display the resulting frame
# cv2.imshow('Input', frame)

# Wait for the user to press any key
cv2.waitKey(0)

# When everything done, release the capture and destroy the windows
cap.release()
cv2.destroyAllWindows()


import cv2
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