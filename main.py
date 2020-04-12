from flask import Flask, render_template, request
from urllib.parse import unquote_plus
from utils import get_best_answers, launch_default_browser
from database import database_to_tree

# Flask App setup
PORT = 5000
app = Flask(__name__)
# Get the KDtree from our database
tree = database_to_tree()


def get_best_answers_dummy():
    return [{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},{"answer": "I am good!", "source":"https://baraha.com/v10/index.php", "distance":10},]

# Home page route
@app.route('/') 
def homepage(): 
    return render_template("index.html")

# Search display route
@app.route('/search')
def search():
    question = unquote_plus(request.args.get("q"))
    answers = get_best_answers(question, 10, tree)
    return render_template("search.html", answers=answers)

# Run the program
if __name__ == '__main__':
    launch_default_browser(PORT)
    app.run(host='127.0.0.1', port=PORT, debug=True)
    