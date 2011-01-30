#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from random import randint
from itertools import imap

#predicate validator
def pv(f):
    def validator(x):
        if not f(x):
            raise ValueError(str(x) + " didn't pass validation")
    return validator

class Person(db.Model):
    name = db.StringProperty()
    addresses = db.ListProperty(str, required=True, validator=pv(lambda l: len(l) > 0))
    rank = db.IntegerProperty(required=True, default=0, validator=pv(lambda x: x >= 0))
    
    def __repr__(self):
        return "<Person %r %r %r %r>" % (self.rank, self.name, self.addresses, list(self.proposal_set))
    
    def __eq__(self, o):
        if type(o) == Person:
            return self.key() == o.key()
        return False
        

class Proposal(db.Model):
    text = db.TextProperty(required=True)
    proposer = db.ReferenceProperty(Person)
    proposed = db.BooleanProperty(default=False, required=True)

def getPeopleWithUnproposedLegislation():
    #first pass, stupid, slow, but hopefully correct
    #obviously this will need to be optimized to scale at all
    unproposed_legislation = db.GqlQuery("SELECT * FROM Proposal WHERE proposed = False")
    return list(set(imap(lambda x: x.proposer, unproposed_legislation)))

def getProposer():
    people_with_unproposed_legislation = getPeopleWithUnproposedLegislation()
    min_rank_person = list(db.GqlQuery("SELECT * FROM Person WHERE key IN :1 ORDER BY rank ASC LIMIT 1", people_with_unproposed_legislation))
    if len(min_rank_person) == 0: 
        return None
    min_people = list(db.GqlQuery("SELECT * FROM Person WHERE rank = :1 AND __key__ in :2", min_rank_person[0].rank, people_with_unproposed_legislation))
    index = randint(0, len(min_people))
    return min_people[index]

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Nothing (yet) to see here, move along!')

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
