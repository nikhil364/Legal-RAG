import requests


OLLAMA_URL = "http://ollama:11434/api/generate"



def generate_answer(prompt):

    response = requests.post(

        OLLAMA_URL,

        json={

            "model":"llama3.1",

            "prompt":prompt,

            "stream":False

        }

    )


    return response.json()["response"]