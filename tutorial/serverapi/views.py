from http.client import HTTPResponse
import json
from rest_framework.response import Response
from rest_framework import status
from tutorial.serverapi.insert_temp import cek_temp_qna, insert_temp_qna, update_temp_qna
from tutorial.serverapi.cek_qna import cek_qna
from tutorial.serverapi.insert_qna import insert_qna
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from .prompting import *
from django.contrib.auth.models import User
import os
import openai
from  tutorial.serverapi.conversation import generate_answer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from langchain.callbacks import get_openai_callback

openai.api_key = os.environ.get("OPENAI_KEY")

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializers = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializers.data})

@api_view(['POST'])
def signup(request):
    serializers = UserSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializers.data})
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"passed for {}".format(request.user.email)})

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def openAIView(request):
    if request.method == 'GET':
        """
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
        """
        return Response(status=status.HTTP_201_CREATED) 

    elif request.method == 'POST':
        question = request.POST['prompt']
        
       
        hasil_cek = cek_qna(question) #cek pertama kali. cek dataset pertanyaan apakah ada yang sama
        hasilout = hasil_cek['message']  #cek kedua kali. cek dulu pertanyaan sudah pernah ada atau tidak di database?, jika sudah ada pakai fungsi untuk mengambil existing question dari database
        hasilout=str(hasilout).strip("()`'',")
        #print(hasilout)
        if(hasilout != 'None'):
            data_obj = openAI(hasilout)
            serializer_class = openAISerializer(data_obj)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else: 
            with get_openai_callback() as cb:
                prompt = generate_answer(question)
                #print(prompt)
                hasil_cek2 = cek_temp_qna(question)
                hasiltemp = hasil_cek2['message']
                hasiltemp = str(hasiltemp).strip("()`'',")
                print(f'hasiltemp ={hasiltemp}')
                if(hasiltemp == 'None'):
                    insert_temp_qna(question,prompt)
                else:
                    update_temp_qna(question,prompt,hasiltemp)
                print(cb)

            data_obj = openAI(prompt)
            serializer_class = openAISerializer(data_obj)
            #
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)

        #cek validasi apakah pertanyaan sudah disimpan sebelumnya.. supaya tdk dobel.
        #simpan pertanyaan ke existing question
        #return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        #return Response(serializer_class.data, status=status.HTTP_201_CREATED)

"""
0. autorhization validation. (done)
1. cek kesamaan output (done)
2.
buat akurasi, berapa salahnya, berapa benarnya untuk mengihtung akurasinya. minmal 25 pertanyaan.
berapa salah, berapa benar.
pertanyaan typo, sesuai dataset, diluar dataset.
3. dihitung kecepatan chat gpt
dataset sekian berapa akecepatan, kalu ditambah dataset itu berapa..
cek dilokal.. untuk kecepatan. dataset 1000. 5 percobaan, percobaan 1, 2,3,4,5 berapa speed lalu di rata rat.
4. dibandingkan pertanyaan yang disimpan, apakah mempengaruhi kecepatan?
"""