import openai
import json
from collections import ChainMap
import sys
from tutorial.serverapi.langchain import chain

chat_history = []
def generate_answer(question):
    global chat_history
    query = "Prompt: "+question
    result = chain({"question": query, "chat_history": chat_history})
    chat_history.append((query, result['answer']))
    return(result['answer'])

"""

# Set global variable untuk menampung seluruh percakapan, konteks awal sebaiknya atur disini
conversation = ChainMap({
      "role": "system",
      "content": "Kamu adalah percakapan asisten pribadi AI di whatsapp berbahasa Indonesia. Asisten tersebut sangat membantu, kreatif, cerdas, dan sangat ramah."
    })

def generate_answer(question):
    global conversation # Ini perlu agar dalam function menganggap conversation sebagai global variable
    user_question = {"role": "user", "content": f"{question}"} # Formating pertanyaan untuk prompt
    conversation.maps.append(user_question) # Gabung percakapan sebelumnya dengan format pertanyaan user agar menjadi percakapan yang lengkap

    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation.maps,
            temperature=0
    )

    assistant_message = response['choices'][0]['message']['content'] # Simpan pesan jawaban dari ChatGPT
    assistant_reply = {"role": "assistant", "content": f"{assistant_message}"} # Formating jawaban
    conversation.maps.append(assistant_reply) # Gabung percakapan sebelumnya dengan format jawaban agar konteks nya tidak hilang
    return(assistant_message)


Lumen generate session id
nannti di
"""