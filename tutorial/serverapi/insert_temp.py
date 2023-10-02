
import numpy as np
import pandas as pd
import csv
import re
import mysql.connector
from tutorial.serverapi.insert_qna import insert_qna
import os


db = mysql.connector.connect(
  host=os.environ.get('DB_HOST'),
  user=os.environ.get('DB_USER'),
  passwd=os.environ.get('DB_PASSWORD')
)

def cek_temp_qna(question):
    if db.is_connected():
        mycursor = db.cursor()
        mycursor.execute("SELECT hitung FROM serverapi_chatbot.temp_qna WHERE pertanyaan LIKE '{}'LIMIT 1;".format(question))
        myresult = mycursor.fetchone()
        if myresult!= "":
            return {'result': True, 'message': myresult}
        else:
            return {'result': False, 'message': 'tidak ada'}

def insert_temp_qna(question,answer):
    if db.is_connected():
        mycursor = db.cursor()
        print(question)
        print(answer)
        mycursor.execute(f"INSERT INTO serverapi_chatbot.temp_qna (pertanyaan,jawaban,hitung) VALUES ('{question}','{answer}','1');")
        db.commit()
        print("succsess")

def update_temp_qna(question,answer,hitung):
    if db.is_connected():
        mycursor = db.cursor()
        print(question)
        print(answer)
        print(hitung)
        hitung=int(hitung)
        hitung = hitung + 1
        print(f"hitung = {hitung}")
        mycursor.execute(f"UPDATE serverapi_chatbot.temp_qna SET hitung = '{hitung}' WHERE (pertanyaan LIKE '{question}');")
        db.commit()
        print("succsess")
        if(hitung == 3):
            insert_qna(question,answer)