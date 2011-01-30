import unittest
import main
from google.appengine.ext import db

class PersonTest(unittest.TestCase):
    
    def test_person_create(self):
        steve = main.Person(name="Steve", addresses=["steveHOLT@example.edu", "rudabega@example.com"], rank=0)
        steve.put()
        people = list(db.GqlQuery("SELECT * FROM Person"))
        self.assertEquals(len(people), 1)
        person = people[0]
        self.assertEquals(steve.name, person.name)
        self.assertEquals(set(steve.addresses), set(person.addresses))
        self.assertEquals(steve.rank, person.rank)
    
    def test_no_address(self):
        try:
            main.Person(addresses=[]).put()
        except ValueError:
            return # yay!
        self.fail("shouldn't allow a person with no addresses")
    
    def test_negative_rank(self):
        try:
            main.Person(addresses=["lol@example.com"], rank=-1).put()
        except ValueError:
            return # yay!
        self.fail("shouldn't allow a person with negative rank")
        