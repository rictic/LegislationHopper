import unittest
from main import Person, Proposal, getNextProposal
import main
from google.appengine.ext import db
from random import random
from itertools import imap

def makePerson(rank, **kwd):
    person = Person(addresses=[str(random())+"@example.com"], rank=rank, **kwd)
    person.put()
    return person
def makeProposal(proposer, **kwd):
    proposal = Proposal(text=str(random), proposer=proposer, **kwd)
    proposal.put()
    return proposal
class GetNextProposalTest(unittest.TestCase):
    
    #no people, no proposals, no options
    def testNothing(self):
        self.assertEquals(None, getNextProposal())
    
    #people, but no proposals, no options
    def testZeroCase(self):
        for i in range(20):
            makePerson(0)
        self.assertEquals(None, getNextProposal())
    
    #if exactly one person has a proposal in the hopper, then that person must be chosen
    def testOneCase(self):
        for i in range(20):
            makePerson(0)
        prop = makeProposal(makePerson(0))
        self.assertEquals(prop, getNextProposal())

    #when multiple people have made proposals, the proposal whose proposer's rank is lowest wins
    def testGetLowestRankProposal(self):
        p1 = makePerson(1)
        p2 = makePerson(2)
        makeProposal(p2)
        prop = makeProposal(p1)
        self.assertEquals(prop, getNextProposal())
    
    #when multiple people have the same rank, the first proposal to be proposed by any of them is chosen
    def testGetEarliestInRankGroup(self):
        p1 = makePerson(1)
        p2 = makePerson(1)
        prop = makeProposal(p2)
        makeProposal(p1)
        makeProposal(p2)
        self.assertEquals(prop, getNextProposal())
    
    #legislation that been proposed should be completely ignored by getNextProposal
    def testIgnoreProposedLegislation(self):
        p1 = makePerson(1)
        p2 = makePerson(2)
        makeProposal(p1, proposed=True)
        makeProposal(p2)
        prop = makeProposal(p1)
        makeProposal(p1)
        self.assertEquals(prop, getNextProposal())

    #if all legislation has been proposed, then there's nothing to propose
    def testAllLegislationProposed(self):
        p1 = makePerson(1)
        p2 = makePerson(2)
        makeProposal(p1, proposed=True)
        makeProposal(p2, proposed=True)
        makeProposal(p1, proposed=True)
        self.assertEquals(None, getNextProposal())
    
    def testAllLowRankLegislationProposed(self):
        p1 = makePerson(1)
        p2 = makePerson(2)
        makeProposal(p1, proposed=True)
        makeProposal(p1, proposed=True)
        prop = makeProposal(p2)
        self.assertEquals(prop, getNextProposal())