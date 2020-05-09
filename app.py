import json
import requests
from flask import Flask,render_template, redirect, request
from covid_india import states
import pickle
import bs4



app = Flask(__name__)


load_model = pickle.load(open('final_model.sav', 'rb'))

@app.route('/')
def index():
    data = requests.get("https://www.mygov.in/covid-19")
    bs = bs4.BeautifulSoup(data.text, 'html.parser')
    active_case= bs.find("div" , class_="information_row").find("div" , class_="iblock active-case").find("span", class_="icount").get_text()
    discharge= bs.find("div" , class_="information_row").find("div" , class_="iblock discharge").find("span", class_="icount").get_text()
    death= bs.find("div" , class_="information_row").find("div" , class_="iblock death_case").find("span", class_="icount").get_text()
    active_case = int(active_case)
    discharge = int(discharge)
    death = int(death)
    confirm = active_case + discharge + death
    state='Gujarat'
    data = states.getdata(state)
    return  render_template('index.html',
                                   title='add text '
                                         'and submit',active_case = active_case ,discharge = discharge ,death = death , confirm = confirm,data=data,state=state)
										 
@app.route('/state/',methods=["POST"])
def search_statte():
    data = requests.get("https://www.mygov.in/covid-19")
    bs = bs4.BeautifulSoup(data.text, 'html.parser')
    active_case= bs.find("div" , class_="information_row").find("div" , class_="iblock active-case").find("span", class_="icount").get_text()
    discharge= bs.find("div" , class_="information_row").find("div" , class_="iblock discharge").find("span", class_="icount").get_text()
    death= bs.find("div" , class_="information_row").find("div" , class_="iblock death_case").find("span", class_="icount").get_text()
    active_case = int(active_case)
    discharge = int(discharge)
    death = int(death)
    confirm = active_case + discharge + death
    if request.method == 'POST':
        state = request.form['state']
        data = states.getdata(state)
        return render_template('index.html',data=data,state=state, active_case = active_case ,discharge = discharge ,death = death , confirm = confirm)

@app.route('/about')
def about():
	return render_template('about.html')
	
@app.route('/contact')
def contact():
	return render_template('contact.html')
	
@app.route('/hwd')
def hwd():
	return render_template('hwd.html')

'''#function to run for prediction
def detecting_fake_news(var):    
  #retrieving the best model for prediction call
  prediction = load_model.predict([var])
  prob = load_model.predict_proba([var])
  stc = "The given statement is {} The truth probability score is {}"
  return stc.format(prob[0][1])
'''
#function to run for prediction
def detecting_fake_news(var):    
  #retrieving the best model for prediction call
  prediction = load_model.predict([var])
  prob = load_model.predict_proba([var])
  if prob[0][1] < 0.6:
      stc = "The given proclamation is false reality probability score is {}"
      stc = stc.format(prob[0][1])
      return stc
  else:
      stc = "The given proclamation is True reality probability score is {}"
      stc = stc.format(prob[0][1])
      if stc=="The given proclamation is True reality probability score is 0.6828804214017451":
          stc="Invalid text"
          return stc
      return stc
  
@app.route('/fetch', methods=['POST'])
def fetch():
    var = request.form["txt"]
    strres = detecting_fake_news(str(var))
    data = requests.get("https://www.mygov.in/covid-19")
    bs = bs4.BeautifulSoup(data.text, 'html.parser')
    active_case= bs.find("div" , class_="information_row").find("div" , class_="iblock active-case").find("span", class_="icount").get_text()
    discharge= bs.find("div" , class_="information_row").find("div" , class_="iblock discharge").find("span", class_="icount").get_text()
    death= bs.find("div" , class_="information_row").find("div" , class_="iblock death_case").find("span", class_="icount").get_text()
    active_case = int(active_case)
    discharge = int(discharge)
    death = int(death)
    confirm = active_case + discharge + death
    state='Gujarat'
    data = states.getdata(state)
    return render_template('fetch.html', strres= strres,active_case = active_case ,discharge = discharge ,death = death , confirm = confirm ,data=data,state=state )

if __name__ == "__main__":
    app.run(debug=True)
