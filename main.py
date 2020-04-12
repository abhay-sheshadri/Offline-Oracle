from flask import Flask, render_template, request
from urllib.parse import unquote_plus
#from utils import get_best_answers, launch_default_browser

PORT = 5000
app = Flask(__name__)

def get_best_answers_dummy():
    return [{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},]

# Launch the user's default browser to localhost:port
def launch_default_browser(port):
    import webbrowser
    url = "http://127.0.0.1:"+str(port)
    return webbrowser.open(url, new=2)

@app.route('/') # this is the home page route
def homepage(): # this is the home page function that generates the page code
    return render_template("index.html")
    
@app.route('/search')
def search():
    question = unquote_plus(request.args.get("q"))
    #answers = get_best_answers(question)
    answers = get_best_answers_dummy()
    return render_template("search.html", answers=answers)
   
if __name__ == '__main__':
    launch_default_browser(PORT)
    app.run(host='127.0.0.1', port=PORT, debug=True)
    
