from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view
from .prompting import *
import os
import openai
from  tutorial.serverapi.conversation import generate_answer

openai.api_key = "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"

@api_view(['GET', 'POST'])


def openAIView(request):
    if request.method == 'GET':
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "kamu adalah asisten tanya jawab tentang teknologi."},
                {"role": "user", "content": "apa itu bahasa PHP!"}
            ]
        )
        prompt = completion.choices[0].message.content
        data_obj = openAI(prompt)
        serializer_class = openAISerializer(data_obj)
        return Response(serializer_class.data) 

    elif request.method == 'POST':
        question = request.POST['prompt']
        print(question)
        prompt = generate_answer(question)
        data_obj = openAI(prompt)
        serializer_class = openAISerializer(data_obj)
        return Response(serializer_class.data, status=status.HTTP_201_CREATED)


"""

def openAIView(request):
    if request.method == 'GET':
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "kamu adalah asisten tanya jawab tentang teknologi."},
                {"role": "user", "content": "apa itu bahasa PHP!"}
            ]
        )
        prompt = completion.choices[0].message.content
        data_obj = openAI(prompt)
        serializer_class = openAISerializer(data_obj)
        return Response(serializer_class.data) 

    elif request.method == 'POST':
        question = request.POST['prompt']
        print(question)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "kamu adalah asisten tanya jawab tentang teknologi."},
                {"role": "user", "content": str(question)}
            ]
        )
        prompt = completion.choices[0].message.content
        data_obj = openAI(prompt)
        serializer_class = openAISerializer(data_obj)
        return Response(serializer_class.data, status=status.HTTP_201_CREATED)

"""