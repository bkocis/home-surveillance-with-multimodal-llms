import cv2
import ollama
import time
import sys


def query_the_image(query: str, image_list: list[str]) -> ollama.chat:
    try:
        res = ollama.chat(
            model='llava',
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


def capture_scene():
    print("Capturing initial scene description....")
    ret, frame = cap.read()
    image = [cv2.imencode('.jpg', frame)[1].tobytes()]
    response = query_the_image("What do you see on the image", image)
    print("Capturing initial scene description....done!")
    return response


def observe_scene_change(initial_scene: str):
    print("Capture frame-by-frame")
    while True:
        time.sleep(5)
        ret, frame = cap.read()
        print(ret)
        image = [cv2.imencode('.jpg', frame)[1].tobytes()]
        query_1 = (f"You are a home surveillance system - "
                 f"you need to observe the image and report very short way with only yes or no "
                 f"if you see something different in the image relative to the initial scene described as '{initial_scene}'. "
                 # f"Don't use any other sentences to describe the image!"
        )
        query_2 = "report very short way with only yes or no - Do you see people in the image?"
        query_3 = "report very short way with only yes or no - Do you see someone steeling something?"
        query_4 = "report very short way with only yes or no - Do you see people moving?"

        print_out_the_response(query_1, image_list=image)
        print_out_the_response(query_2, image_list=image)
        print_out_the_response(query_3, image_list=image)
        print_out_the_response(query_4, image_list=image)



def print_out_the_response(query_message: str, image_list: list[str]) -> None:
    response = query_the_image(query_message, image_list)
    if response:
        print(response)
        sys.stdout.flush()
        sys.stdout.write("\n")


if __name__ == "__main__":

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    scene_description = capture_scene()

    observe_scene_change(initial_scene=scene_description)

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