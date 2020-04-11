import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import tensorflow_text
from kdtree import KDTree


module = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3") # Our model

# Takes in a list of questions and returns numpy arrays of their embeddings
def get_question_embeddings(questions):
    global module
    question_embeddings = module.signatures["question_encoder"](
        tf.constant(questions)
    )
    return question_embeddings["outputs"].numpy().astype(np.float32)

# Takes in a list of responses and returns numpy arrays of their embeddings
def get_response_embeddings(responses):
    global module
    response_embeddings = module.signatures["response_encoder"](
        input = tf.constant(responses),
        context = tf.constant(responses)
    )
    return response_embeddings["output"].numpy().astype(np.float32)

"""

questions = ["What is your age?"]
responses = ["I am very young.", "I am 4 years old.", "I am an American.", " I am a brown boy."]

question_embeddings = module.signatures["question_encoder"](
    tf.constant(questions)
)

response_embeddings = module.signatures["response_encoder"](
    input=tf.constant(responses),
    context=tf.constant(responses)
)

res = []
ponses = response_embeddings["outputs"].numpy()

for i in range(len(ponses)):
    res.append({
        "vector": ponses[i],
        "sentence": responses[i],
        "source": "https://www.baraha.com"
    })

tree = KDTree(res, 512)
answer = tree.get_best_vectors(
    question_embeddings["outputs"].numpy()[0],
    2
)

for ans in answer:
    print(ans[1]["sentence"], ans[0])
"""
