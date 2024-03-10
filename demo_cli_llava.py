import cv2
import ollama
import datetime


def query_the_image(query: str, image_list: list[str]) -> ollama.chat:
    try:
        res = ollama.chat(
            model='llava:7b-v1.6-mistral-q2_K',
            options={
                'temperature': 0,
                "top_k": 1,
                'top_p': 0.1,
                'mirostat_tau': 1.0,
                'num_ctx': 1024,
                'seed': 42,
                'num_predict': 128
            },
            messages=[
                {
                    'role': 'system',
                    'content': "You are a home surveillance system. Answer with very short sentences."
                },
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


def observe_scene_change(initial_scene: str, image) -> None:
    queries = [
        "Do you see people in the image?",
        "Do you see someone stealing something?",
        "Do you see people moving?",
        "Is there any dog in the frame?"
        ]
    for query in queries:
        print_out_the_response(query, image_list=image)


def print_out_the_response(query_message: str, image_list: list[str]):
    response_llava = query_the_image(query_message, image_list)
    timestamp = str(datetime.datetime.now())
    response = {
        "timestamp": timestamp,
        "question": query_message,
        "answer": response_llava
    }
    print(response)
    return response


def image_processing_function(frame) -> None:
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = [cv2.imencode('.jpg', frame)[1].tobytes()]
    pass_image_to_llava(image)


def pass_image_to_llava(image) -> None:
    scene_description = query_the_image("What is on the image?", image_list=image)
    observe_scene_change(initial_scene=scene_description, image=image)


def frame_generator(cap: cv2.VideoCapture, debug_show_image: bool):
    """
    This function reads the data from the camera and yields them frame-by-frame
    :param cap:
    :param debug_show_image: set to True for visual debugging
    :yield: frame and frame counter
    """
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_number += 1
        if debug_show_image:
            cv2.imshow('Webcam Live', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        yield frame_number, frame


def display_frame_generator(
        cap: cv2.VideoCapture, image_processing_function: callable, every_nth_second: int, debug_show_image: bool
) -> None:
    frame_rate = 30
    for frame_number, frame in frame_generator(cap, debug_show_image):
        if frame_number % (every_nth_second * frame_rate) == 0:
            image_processing_function(frame)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    evaluate_a_frame_in_n_seconds = 1

    display_frame_generator(
        cap,
        image_processing_function=image_processing_function,
        every_nth_second=evaluate_a_frame_in_n_seconds,
        debug_show_image=True
    )
