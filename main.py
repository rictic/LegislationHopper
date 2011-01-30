#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from random import randint
from itertools import imap, groupby

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
    proposed_on = db.DateTimeProperty(auto_now_add=True)
    
    def __eq__(self, o):
        if type(o) == Proposal:
            return self.key() == o.key()
        return False

def getNextProposal():
    people = list(db.GqlQuery("SELECT * FROM Person ORDER BY rank ASC"))
    for rank, rankGroup in groupby(people, lambda p: p.rank):
        proposal = getEarliestPropsalBy(rankGroup)
        if proposal is not None:
            return proposal
    return None

def getEarliestPropsalBy(people):
    proposal = list(db.GqlQuery("SELECT * FROM Proposal WHERE proposer IN :1 AND proposed = False ORDER BY proposed_on ASC LIMIT 1", getKeys(people)))
    if len(proposal) == 0:
        return None
    return proposal[0]

def getKeys(entities):
    return list(map(lambda e: e.key(), entities))

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Nothing (yet) to see here, move along!')

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
