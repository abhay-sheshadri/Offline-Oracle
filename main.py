from flask import Flask, render_template, request
from urllib.parse import unquote_plus
from utils import get_best_answers, launch_default_browser

PORT = 5000
app = Flask(__name__)

@app.route('/') # this is the home page route
def homepage(): # this is the home page function that generates the page code
    return render_template("index.html")
    
@app.route('/search')
def search():
    question = unquote_plus(request.args.get("q"))
    answers = get_best_answers(question)
    return render_template("search.html", answers=answers)
   
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=PORT, debug=True)
    launch_default_browser(PORT)
