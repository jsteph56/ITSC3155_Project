#ITSC3155 Project

#Imports
import os
from flask import Flask
from flask import render_template


#Create the app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
