import discord
from flask import Flask
from threading import Thread
import os

os.system("pip3 install pymongo[srv]")

app = Flask('')



@app.route('/')
def home():
  return "Status: active"

def run():
  app.run(host='0.0.0.0',port=8080)

def start():
  t = Thread(target=run)
  t.start()