
import numpy as np
import pandas as pd
import csv
import re
import mysql.connector
import os

db = mysql.connector.connect(
  host=os.environ.get('DB_HOST'),
  user=os.environ.get('DB_USER'),
  passwd=os.environ.get('DB_PASSWORD')
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
