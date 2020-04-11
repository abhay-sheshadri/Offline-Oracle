import sqlite3 as sql
import numpy as np
import io
from kdtree import KDTree

# The database code

conn = sql.connect("responses.db", detect_types=sql.PARSE_DECLTYPES)
c = conn.cursor()

# Adapters
def adapt_array(array):
    out = io.BytesIO()
    np.save(out, array)
    out.seek(0)
    return sql.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

sql.register_adapter(np.ndarray, adapt_array)
sql.register_converter("array", convert_array)

# Creates the SQL table
def create_table(dim):
    global c
    c.execute("CREATE TABLE IF NOT EXISTS responseData(sentence TEXT, source TEXT, arr array)")

# Adds an entry into the database
def add_entry(sentence, source, vector):
    global c
    c.execute("INSERT INTO responseData (sentence, source, arr) VALUES(?, ?, ?)", (sentence, source, vector))
    conn.commit()

# Inputs multiple entries
def add_multiple_entries(array, window=10):
    for i in range(len(array)):
        sentence, source, vector = array[i]
        c.execute("INSERT INTO responseData (sentence, source, arr) VALUES(?, ?, ?)", (sentence, source, vector))
        if (i + 1) % window:
            conn.commit()

# Checks if the sentence is in the database
def is_in_database(sentence):
    c.execute("SELECT sentence FROM responseData WHERE sentence == ?", (sentence,) )
    if c.fetchall():
        return True
    return False

# Remove an entry
def remove_entry(sentence):
    c.execute("DELETE FROM responseData WHERE sentence == ?", (sentence,) )
    conn.commit()

# Removes multiple entries
def remove_multiple_entries(array, window=10):
    for i in range(len(array)):
        c.execute("DELETE FROM responseData WHERE sentence == ?", (array[i],) )
        if (i + 1) % window:
            conn.commit()

# Database to KDTree
def database_to_tree(dim=512):
    c.execute("SELECT * FROM responseData")
    res = []
    for sentence, source, vector in c.fetchall():
        res.append({
            "sentence": sentence,
            "source": source,
            "vector": vector
        })
    return KDTree(res, dim) 

# Run on close
def close_database():
    global c, conn
    c.close()
    conn.close()
