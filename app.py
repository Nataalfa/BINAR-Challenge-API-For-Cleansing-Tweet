import pandas as pd
# import main Flask class and request object
from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
from Clean import  process_text, process_csv
import sqlite3

#Database
db =  sqlite3.connect('Gold Challenge.db', check_same_thread=False)
db.row_factory = sqlite3.Row
Cursor = db.cursor()

# create the Flask app
app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'Binar Challenge Gold Chapter'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Tweet yang sudah di cleansing menggunakan ReGex'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)


@swag_from("docs/home.yaml", methods=['GET'])
@app.route('/', methods=['GET'])
def get():
    return "Challenge Gold Chapter"
    
# Tweet
@swag_from("docs/tweet.yaml", methods=['GET'])
@app.route("/tweet", methods=['GET'])
def tweet():
    query_text = "SELECT * FROM Clean_tweet"
    select_tweet = Cursor.execute(query_text)
    tweet = [
        dict(id=row[0], Tweet=row[1], Clean_tweet=row[2])
        for row in select_tweet.fetchall()
    ]
    # Define API response
    json_response = [
        {
            'status_code': 200,
            'description': "Tweet yang sudah di cleansing",
            'tweet': tweet,
        }
    ]
    response_data = jsonify(json_response)    
    return response_data

@swag_from("docs/tweet_text.yaml", methods=['POST'])
@app.route("/tweet_text", methods=['POST'])
def tweet_text():
    input_text = str(request.form["text"])
    output_text = process_text(input_text)

    query_text = "insert into Clean_tweet (Tweet, Clean_tweet) values(?, ?)"
    val = (input_text, output_text)
    Cursor.execute(query_text, val)
    db.commit()
    # Define API response
    json_response  = [
        {
        'status_code': 200,
        'description': "Tweet has been cleaned ",
        'Inputed_text': input_text,
        'Clean_Output': output_text,
        }
    ]
    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/tweet_file.yaml", methods=['POST'])
@app.route("/tweet_file", methods=['POST'])
def tweet_file():
    file = request.files['file']

    df = pd.read_csv(file,header=0)
    df_list = df.Tweet.to_list()
    
    process_csv(df)
    # Define API response
    json_response = [
        {
        'status_code': 200,
        'description': "Input CSV File success",
        'data': df_list,
        }
    ]

    response_data = jsonify(json_response)   
    
    return response_data


if __name__ == '__main__':
    # run app in debug mode on port 4000
    app.run(host='0.0.0.0',debug=True, port=4000)

