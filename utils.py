import numpy as np
import webbrowser
import embeddings

# Gets the best answers
def get_best_answers(question, count, tree):
    vec = embeddings.get_question_embeddings([question,])[0]
    ans = tree.get_best_vectors(vec, count)
    answers = []
    # Creating a json
    for answer in ans:
        answers.append({
           "answer": answer[1]["sentence"],
           "source": answer[1]["source"],
           "distance": answer[0]
        })
    return answers

# Launch the user's default browser to localhost:port
def launch_default_browser(port):
    url = "http://127.0.0.1:"+str(port)
    return webbrowser.open(url, new=2)