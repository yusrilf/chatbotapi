
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

def insert_qna(question,answer):
    if db.is_connected():
        mycursor = db.cursor()
        print(question)
        print(answer)
        mycursor.execute(f"INSERT INTO serverapi_chatbot.qna (pertanyaan,jawaban) VALUES ('{question}','{answer}');")
        db.commit()
        print("succsess")