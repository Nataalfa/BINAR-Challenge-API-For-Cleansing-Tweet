# BINAR-Challenge-API-For-Cleansing-Tweet
This API will cleansing input text and show the output the clean text and input and output text will uploaded to sqlite3 database 

## Requirements 
<b>Install requirements
run on your terminal prompt:</b>
`pip install -r requirements.txt` 

## Create Cleansing Fucntion 
First, make function to lower case all character from the text and make function for cleansing unnecessary character like RT, USER, URL, and etc. 
- <b>e.g :</b>
 - `def lowercase(text):
     return text.lower()`

 - `def remove_unnecessary_char(text):
     text = re.sub('\n',' ',text) 
     text = re.sub('rt',' ',text) 
     text = re.sub('user',' ',text) 
     text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) 
     text = re.sub('  +', ' ', text) 
     return text`

For more function you can check on <b>[Clean.py](https://github.com/Nataalfa/BINAR-Challenge-API-For-Cleansing-Tweet/blob/main/Clean.py)</b> file 

## Connect to database and Making Restful API
- import database to <b>app.py</b> file:
    - `import sqllite3`
    - <b>connect to sqlite3</b> 
        - `db =  sqlite3.connect('Gold Challenge.db', check_same_thread=False)
           db.row_factory = sqlite3.Row
           Cursor = db.cursor()`

- Create the Flask app:
    - `app = Flask(__name__)` for further steps check on <b>[app.py](https://github.com/Nataalfa/BINAR-Challenge-API-For-Cleansing-Tweet/blob/main/app.py)</b> file

- run the API on your local host by write this command on terminal : `python app.py`