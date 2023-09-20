import numpy as np
import pandas as pd
import csv
import re
import mysql.connector

db = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="password"
)

def cek_qna(question):
    if db.is_connected():
        mycursor = db.cursor()
        mycursor.execute("SELECT Jawaban FROM serverapi_chatbot.qna WHERE pertanyaan LIKE '%{}%'LIMIT 1;".format(question))
        myresult = mycursor.fetchone()
        if myresult!= "":
            return {'result': True, 'message': myresult}
        else:
            return {'result': False, 'message': 'tidak ada pertanyaan yang sama'}
