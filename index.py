#!/usr/bin/python
# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*
from flask import Flask,redirect, url_for, render_template, request, session, flash

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import platform
from webdriver_manager.chrome import ChromeDriverManager


# detect os system
os = platform.system()
if os=="Linux":
    path =r"driver"
else:
    path =r"driver.exe"

options = Options()
options.headless = True


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.minimize_window()

app = Flask(__name__)

# ტოკენი
app.secret_key = "app" 



def get_words(count,topic):
    if topic  == "<>":
        return ["<>","<>"]
    else:
        driver.get(f"https://relatedwords.org/relatedto/{topic}")
        time.sleep(0.2)
        # count+=1
        try:
            items = driver.find_elements(By.CLASS_NAME, "item")
            words=[]
            for i in range(3, len(items)): # მესამე სიტყვიდანს
                if count > 0 :
                   count-=1              
                   words.append(items[i].text)                     
                else:
                   break
        except:
            pass
            print(f"{topic} - word break")
        return words


# root directory decorator
@app.route("/", methods=["POST","GET"])
def choose_topic():
    if request.method == "POST":
        topic = request.form["topic"]
        session["topic"] = topic
        return redirect(url_for("choose"))
    else:
        if "topic" in session:
            session.pop("topic")
        return render_template("index.html")

@app.route("/choose")
def choose():   
    if "topic" in session:
        return redirect(url_for("map"))
    else:
        return redirect(url_for("choose_topic"))


@app.route("/map")
def map():
    topic = session["topic"] 
    words_1 = get_words(2,topic) # 2
    words_2 = [
    get_words(2,words_1[0]), 
    get_words(2,words_1[1])] # 4
    words_3 = [
    get_words(2,words_2[0][0]),
    get_words(2,words_2[0][1]), 
    get_words(2,words_2[1][0]), 
    get_words(2,words_2[1][1])] # 6

    return render_template( "map.html",topic=topic, topics_1=words_1,  topics_2=words_2, topics_3 = words_3)


if __name__ == "__main__":
    app.run()