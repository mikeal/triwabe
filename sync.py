import couchquery
import couchdbviews
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
design_dir = os.path.join(this_directory, 'design')

def sync(db):
    for d in os.listdir(design_dir):
        db.sync_design_doc(d, os.path.join(design_dir, d), language="python")

if __name__ == "__main__":
    sync(couchquery.Database('http://localhost:5984/blog'))