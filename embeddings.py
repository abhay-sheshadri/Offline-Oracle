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
    return response_embeddings["outputs"].numpy().astype(np.float32)

"""

questions = ["What is your age?"]
responses = [ "Hours before, the U.S. surpassed 2,000 coronavirus deaths in a day for the first time, and soon became the country with the most coronavirus deaths, passing Italy's death toll.", 'Worldwide, there are at least 1,700,000 million cases and 109,000 deaths, according to data compiled by Johns Hopkins University.', 'At least 409,000 people have recovered worldwide.', 'The incubation period means the time between catching the virus and beginning to have symptoms of the disease. Most estimates of the incubation period for COVID-19 range from 1-14 days, most commonly around five days.', 'People with COVID-19 generally develop signs and symptoms, including mild respiratory symptoms and fever, on an average of 5 to 6 days after infection.', 'The mean incubation period is 5 to 6 days and the range is 1 to 14 days.', 'COVID-19 is spreading from person to person in parts of the United States.', 'The virus that causes COVID-19 probably emerged from an animal source, but is now spreading from person to person.', 'People can help protect themselves from respiratory illness with everyday preventive actions such as avoiding close contact with sick people and touching your face with unwashed hands, and cleaning your hand frequently.', 'There is currently no vaccine to protect against COVID-19.', 'There is no specific antiviral treatment for COVID-19.', 'People with COVID-19 can seek medical care to help relieve symptoms.', 'You should stay home when you are sick.', 'Older adults and people of any age who have serious underlying medical conditions may be at higher risk for more serious complications from COVID-19.', 'Fear and anxiety about COVID-19 can cause people to avoid or reject others even though they are not at risk for spreading the virus.', 'The symptoms of COVID-19 are fever, cough, and shortness of breath.']

question_embeddings = get_question_embeddings(questions)

ponses = get_response_embeddings(responses)

res = []

for i in range(len(ponses)):
    res.append({
        "vector": ponses[i],
        "sentence": responses[i],
        "source": "https://www.baraha.com"
    })

tree = KDTree(res, 512)
answer = tree.get_best_vectors(
    question_embeddings[0],
    2
)

for ans in answer:
    print(ans[1]["sentence"], ans[0])

"""