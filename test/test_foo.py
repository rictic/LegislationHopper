import unittest
import main
from google.appengine.ext import db

class PersonTest(unittest.TestCase):
    
    def test_personCreate(self):
        steve = main.Person(name="Steve", addresses=["steveHOLT@example.edu", "rudabega@example.com"])
        steve.put()
        people = list(db.GqlQuery("SELECT * FROM Person"))
        self.assertEquals(len(people), 1)
        person = people[0]
        self.assertEquals(steve.name, person.name)
        self.assertEquals(set(steve.addresses), set(person.addresses))
