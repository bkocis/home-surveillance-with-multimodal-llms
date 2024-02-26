import ollama
import sys


def query_the_image(query: str, image_list: list[str]) -> ollama.chat:
    try:
        res = ollama.chat(
            model=selected_model,
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


def print_out_the_response(query_message: str, image_list: list[str]) -> None:
    response = query_the_image(query_message, image_list)
    if response:
        print(response)
        sys.stdout.flush()
        sys.stdout.write("\n")


if __name__ == "__main__":
    selected_model = "llava"
    image_list = []
    print("Type /load <image_path> to load an image, and 'quit' to exit.")
    while True:
        query_message = input(f"Type a command, or a question to image {image_list}:")
        if query_message.lower() == 'quit':
            break
        if query_message.startswith("/load"):
            new_image = query_message.split("/load")[1].strip()
            image_list = [new_image]
            query_message = input("Ask anything about the image: ")
            print_out_the_response(query_message, image_list)
        if not image_list:
            print("Give an image path after writing /load :\n")
        if query_message == '':
            print("Ask another question:")
        if query_message != '' and image_list != []:
            print_out_the_response(query_message, image_list)
