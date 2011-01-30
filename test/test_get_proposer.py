import unittest
from main import Person, Proposal, getProposer
import main
from google.appengine.ext import db
from random import random
from itertools import imap

def makePerson(rank):
    person = Person(addresses=[str(random())+"@example.com"], rank=rank)
    person.put()
    return person
def makeProposal(proposer):
    proposal = Proposal(text=str(random), proposer=proposer)
    proposal.put()
    return proposal
class GetProposerTest(unittest.TestCase):
    
    #if noone has a proposal in the hopper, then noone can be chosen
    def testZeroCase(self):
        for i in range(20):
            makePerson(0)
        self.assertEquals([], list(db.GqlQuery("SELECT * FROM Proposal")))
        self.assertEquals([], main.getPeopleWithUnproposedLegislation())
        self.assertEquals(None, getProposer())
    
    #if exactly one person has a proposal in the hopper, then that person must be chosen
    def testOneCase(self):
        for i in range(20):
            makePerson(0)
        p = makePerson(0)
        makeProposal(p)
        self.assertEquals([p], main.getPeopleWithUnproposedLegislation())
        self.assertEquals(p.key(), getProposer().key())
        
