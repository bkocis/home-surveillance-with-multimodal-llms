
---

## Home surveillance with Ollama

__Can LLMs be used to analyze video feed?__

Models
======

- [LlaVa with ollama](https://ollama.com/library/llava)
- [Moondream2 with transformers](https://github.com/vikhyat/moondream)
  

#### Description

A video stream from a web-camera is fed into a multimodal LLM. Every nth frame is then captioned. Additional questions can be 
added, to get more textual description about an image. For this case it is assumed that the web camera is stationary and 
has the purpose to observe a scene. 

Ollama offers a platform for hosting Large Language Models on your own hardware. You can choose from ollama's ever-growing
model library of latest LLMs. 

One of the models is LlaVa (Large language Visual Assistant). LLaVa is a multimodal model, which allows the user to
caption and understand images. Given an image it can describe it, extract information, and on top of that - to use its
knowledge and context to "chat with the image".

A quantized versions of LlaVa are readily available. Here we will be using a
[**4Bit** quantized version of the **Llava 1.6** model](https://ollama.com/library/llava/tags).

#### Installation

For the purpose of this demo, we will use a small (7b) model with 2Bit quantization. 
After installing `ollama`, the specific model can be downloaded by the following command:

`ollama run llava:7b-v1.6-mistral-q2_K`

List out `ollama` models on your local: 

`ollama list`

Once the model is available, running the python app will load the models in the `ollama.chat` method. 

Additional packages are required, in requirements.txt

#### Running the application

This app demonstrated the applicability of the multimodal LLM for "real time" evaluation of video-feed. The results of 
the model are in this case just dumped into the std output. 
Run the application (after setting up a venv and sourcing it):

`python demo_cli_llava.py`



