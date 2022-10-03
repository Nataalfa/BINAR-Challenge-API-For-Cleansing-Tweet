import pandas as pd 
import re
import sqlite3
db = sqlite3.connect('Gold Challenge.db', check_same_thread=False)


make_table = db.execute("""CREATE TABLE IF NOT EXISTS Clean_tweet (id INTEGER PRIMARY KEY AUTOINCREMENT
,Tweet, Clean_Tweet)""")
db.text_factory = bytes
cursor = db.cursor()

def lowercase(text):
    return text.lower()

def remove_unnecessary_char(text):
    text = re.sub('\n',' ',text) # Remove every '\n'
    text = re.sub('rt',' ',text) # Remove every retweet symbol
    text = re.sub('user',' ',text) # Remove every username
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) # Remove every URL
    text = re.sub('  +', ' ', text) # Remove extra spaces
    return text

def remove_nonaplhanumeric(text):
    text = re.sub('[^0-9a-zA-Z]+', ' ', text) 
    return text


#For Cleansing Data 
def preprocess(text):
    text = lowercase(text) # 1
    text = remove_nonaplhanumeric(text) # 2
    text = remove_unnecessary_char(text) # 2
    return text

#Processs File 
def process_csv(input_file):
    first_column = input_file.iloc[:, 1]
    print(first_column)

    for tweet in first_column:
        clean_tweet = preprocess(tweet)
        query_tabel = "insert into Clean_tweet (Tweet, Clean_tweet) values (?, ?)"
        val = (tweet, clean_tweet)
        cursor.execute(query_tabel, val)
        db.commit()


#For Text Process
def process_text(input_text):
    output_text = preprocess(input_text)
    return output_text



