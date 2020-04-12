from flask import Flask, render_template, request
from urllib.parse import unquote_plus
from utils import get_best_answers, launch_default_browser
import database
import googledrive
import time
import threading

# Flask App setup
PORT = 5000
app = Flask(__name__)
# Get the KDtree from our database
conn, c = database.open_database()
tree = database.database_to_tree(c)
drive = None
running = True

def thread_function():
    global tree, running, drive
    conn, c = database.open_database()
    while running:
        if googledrive.check_internet():
            if drive == None:
                drive = googledrive.auth()
            changes = googledrive.get_different(drive)
            sorted(changes)
            for change in changes:
                database.update_database_with_file(c, conn, change)
            tree = database.database_to_tree(c)
        if running:
            time.sleep(30) # Check once every minute
    database.close_database(c, conn)

# Internet checker thread
thread = threading.Thread(target=thread_function)
thread.start()

# Home page route
@app.route('/') 
def homepage(): 
    return render_template("index.html")

# Search display route
@app.route('/search')
def search():
    question = unquote_plus(request.args.get("q"))
    print(question)
    answers = get_best_answers(question, 10, tree)
    return render_template("search.html", answers=answers)

@app.route("/shutdown")
def shutdown():
    global running, thread, c, conn
    running = False
    thread.join()
    database.close_database(c, conn)
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        return
    func()
    return "shutting down"



# Run the program
if __name__ == '__main__':
    launch_default_browser(PORT)
    app.run(host='127.0.0.1', port=PORT)
