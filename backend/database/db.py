from flask_mongoengine import MongoEngine

db = MongoEngine()

def initialize_db(app):
    db.connect('puskesmas', username='puskesmas', password='puskesmba', authentication_source='puskesmas')