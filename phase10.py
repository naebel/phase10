# Phase 10

# Phase 10 is a card game where players try to create particular sets or runs of
# numbers with their hand of
# 10 cards (https://en.wikipedia.org/wiki/Phase_10). Cards are numbered 1-12
# (ignore card colors, skips and wilds). There are eight of every card for a
# total of 96 cards.
#
# Create a function or method that, when given a hand of 10 cards from the deck,
# returns all phases the
# hand meets. A phase is met if the hand contains at least the phase
# requirements. The phases are:
# Phase 1: 2 sets of 3
# Phase 2: 1 set of 3 + 1 run of 4
# Phase 3: 1 set of 4 + 1 run of 4
# Phase 4: 1 run of 7
# Phase 5: 1 run of 8
# Phase 6: 1 run of 9
# Phase 7: 2 sets of 4
# Phase 8: 7 cards of one color (Ignore this phase)
# Phase 9: 1 set of 5 + 1 set of 2
# Phase 10: 1 set of 5 + 1 set of 3
# Set: multiple cards of the same value
# Run: multiple cards in consecutive ascending order
# For example, if the hand contains the cards 1, 2, 3, 4, 5, 6, 7, 8, 8, and 8,
# the function should indicate
# that phases 2, 4, and 5 are met.
# • Phase 2 is met because there is a set of three 8's and there is at least one
# run of four in the
# remaining cards: 1-4, 2-5, 3-6, or 4-7.
# • Phase 4 is met because there is at least one run of seven: 1-7, or 2-8.
# • Phase 5 is met because there is a run of 8: 1-8.
# Note that the same card cannot be reused within different sets or runs in the
# same phase. For example,
# in phase 2, the same "8" card cannot be used for the set of 3 and again for
# the run of 4.

import os
import sys
import random
import argparse

class Deck:
    def __init__(self):
        # Creates a deck of phase 10 cards sans Skips and Wilds
        self.deck = []
        numOfEachCard = 8
        for i in range(1,13):
            for j in range(numOfEachCard):
                self.deck.append(i)
        random.shuffle(self.deck)

    def shuffleDeck(self):
        random.shuffle(self.deck)

    def createHand(self):
        if not self.deck:
            print("Deck is Empty.")
            return []
        hand = []

        while len(self.deck) > 0 and len(hand) < 10:
            hand.append(self.deck.pop())

        return hand

class Player:
    def __init__(self, newHand=[]):
        self.hand = []
        self.setHand(newHand)

    def getHand(self):
        return self.hand

    def setHand(self, newHand):
        self.hand = []
        if isinstance(newHand, list):
            for item in newHand:
                try:
                    self.hand.append(int(item))
                except:
                    self.hand = []
                    raise ValueError(f"'{item}' is not a valid card. Valid cards are numbers 1-12")
            if len(self.hand) != 10:
                numCards = len(self.hand)
                self.hand = []
                raise ValueError(f"Error: {numCards} cards specified. \n"
                       "Please make sure you enter 10 numbers. No more, no less.")
            try:
                self._getCounts()
            except Exception as e:
                self.hand = []
                raise e
        else:
            raise TypeError("Cannot set hand. Must be a list.")
        self.hand.sort()

    def _getCounts(self):
        counts = {}
        for i in range(1,13):
            counts[i] = 0

        for card in self.hand:
            if card not in counts:
                raise ValueError(f"Card '{card}' outside of range 1 through 12.")
            counts[card] += 1
            if counts[card] > 8:
                raise ValueError(f"Too many '{card}'s. Only 8 cards per number exist.")

        return counts

    def _getSets(self):
        counts = self._getCounts()
        sets = {'above5':[], '5':[], '4':[], '3':[], '2':[]}
        for count in counts:
            if counts[count] > 5:
                sets['above5'].append(count)
            elif counts[count] == 5:
                sets['5'].append(count)
            elif counts[count] == 4:
                sets['4'].append(count)
            elif counts[count] == 3:
                sets['3'].append(count)
            elif counts[count] == 2:
                sets['2'].append(count)
        return sets

    def _getRuns(self):
        runs = []
        curRun = []
        curCard = 0
        for card in self.hand:
            if not curCard:
                curCard = card
            if not curRun:
                curRun.append(card)
                curCard = card
            else:
                if curCard == card:
                    #ignoring other cards in set
                    continue
                if card == curCard + 1:
                    curRun.append(card)
                    curCard = card
                else:
                    if len(curRun) >= 4:
                        runs.append(curRun)
                    curRun = [card]
                    curCard = card
        if curRun and len(curRun) >= 4:
            runs.append(curRun)

        return runs

    def _checkRunsWithSets(self, run, sets):
        # Takes a run (which is a list of the run) and a list of numbers that have sets
        # return True if run works with set
        setsInRun = []
        for i in range(len(run)):
            if run[i] in sets:
                setsInRun.append(run[i])
                if i >= 4 or len(run) - i - 1 >= 4:
                    return True
        if len(setsInRun) == len(sets):
            # all sets are in run and don't cut the run in a workable way
            return False
        return True

    def phasesFullfilled(self):
        # Returns phases fullfilled by current hand of player.
        sets = self._getSets()
        runs = self._getRuns()
        # Possible elimination/combinations for runs:
        #   Run of 9 cannot have any sets above 2
        #   Run of 8 could possibly have a set of 3 meaning phase 2+5+4
        #   Run of 7 could possibly have a set of 4 meaning phase 2+3+4
        phases = set()
        for run in runs:
            if len(run) >= 9:
                #impossible for there to be any other phases (Other than straight runs).
                return {4,5,6}
            elif len(run) == 8:
                # Only possible for phase 2 to also work with a run of 8
                if sets['3']: # only 2 extra cards in hand
                    phases.add(2)
                phases.update([4,5])
                return phases
            elif len(run) == 7: # only 3 extra cards in hand
                # Only possible for phases 2 and 3 to also work with a run of 7
                if sets['3'] or sets['4']:
                    phases.add(2)
                    if sets['4']:
                        phases.add(3)
                phases.add(4)
                return phases

        # Checking for mixes of sets and runs
        if sets['above5'] or sets['5'] or sets['4'] or sets['3']:
            if runs: # all runs in runs are made up of 4 or above
                phasesFound = False
                for run in runs:
                    if sets['above5'] or sets['5']:#have enough extra in set to fit into run
                        phases.update([2,3])
                        break
                    if sets['4']:
                        if self._checkRunsWithSets(run, sets['4']):
                            phases.update([2,3])
                            break
                        else:
                            phases.add(2)
                    if sets['3'] and self._checkRunsWithSets(run, sets['3']):
                        phases.update([2])

        # Now to just check for set combos.
        if len(sets['5']) > 1 or ((sets['5'] or sets['above5']) and sets['4']):
            phases.update([1,7,9,10])
        elif sets['above5']:
            phases.add(1)
            counts = self._getCounts()
            for count in counts:
                if counts[count] == 7:
                    phases.add(9)
                elif counts[count] >= 8:
                    phases.update([7,9,10])
        elif sets['5'] or sets['above5']:
            if sets['3']:
                phases.update([1,9,10])
            elif sets['2']:
                phases.update([9])
        elif len(sets['4']) > 1:
            phases.update([1,7])
        elif len(sets['3']) > 1 or (sets['3'] and sets['4']):
            phases.add(1)

        return phases


def main(args):
    print("\nWelcome to this Phase 10 hand checker!\n")
    keepGoing = True
    luckyQuips = ["Feeling lucky, I see.\n",
                  "Are you sure about that? Well, too late.\n",
                  "If you say so...\n",
                  "May the odds be ever in your favor!\n",
                  "The odds of getting a phase delt to you is less than 1%...\n",
                  "The odds of getting a phase delt to you are very very low...\n",
                  "Here goes nothing!\n",
                  "Never tell you the odds, you say?\n",
                  "Leaving it to fate, I see.\n",
                  "If you want to win a bet, guess no phases. You'll probably win.\n",
                  "Thoughts and prayers to you.\n"]

    while keepGoing:
        print("\n-------------------------------------------------------------\n")
        print("You can test a specific hand, or we'll give you a random hand.\n"
              "Do you have a specific hand in mind? [y/n/exit]")

        userResponse = str(input())
        userResponse = userResponse.strip().lower()

        player = None

        if userResponse == 'exit':
            keepGoing = False
            continue
        elif userResponse == 'y':
            print("Please enter 10 space separated numbers in the range of 1-12 "
                  "(no more than 8 duplicates of any number):")
            requestedHand = str(input())
            if requestedHand.lower() == 'exit':
                keepGoing = False
                continue
            requestedHand.strip()
            requestedHand = requestedHand.split()

            try:
                player = Player(requestedHand)
            except Exception as e:
                print(e)
                continue

        else:
            if userResponse != 'n':
                print("Think you're funny, eh? Well, you didn't say yes, or "
                "exit, so we'll just give you a random hand.")
            else:
                print(luckyQuips[random.randrange(len(luckyQuips))])

            d = Deck()
            player = Player(d.createHand())

        try:
            print(f"Your hand: {player.getHand()}")
            phases = player.phasesFullfilled()
            if phases:
                print(f"Congratulations! Phases found: {phases}")
            else:
                print(f"Nice try. No phases found for this hand. Better luck next time.")
        except Exception as e:
            print("Something weird happened....")
            print(str(e))

def test(args):
    # d = Deck()
    p1 = Player([1,2,3,5,6,8,9,10,12,12])
    testsFailed = False

    #Test no phase found
    print("\nTest no phase found:")
    r1 = p1.phasesFullfilled()
    if not r1:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r1}\nExpected zero phases.")

    # Test runs
    print("\nTest run of 9:")
    p1.setHand([4,5,6,7,8,9,10,11,12,12])
    r2 = p1.phasesFullfilled()
    print(isinstance(r2,set))
    if r2 == {4,5,6}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r2}\nExpected phases 4, 5, and 6")

    print("\nTest run of 9 (full 10):")
    p1.setHand([3,4,5,6,7,8,9,10,11,12])
    r3 = p1.phasesFullfilled()
    if r3 == {4,5,6}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r3}\nExpected phases 4, 5, and 6")

    print("\nTest run of 8:")
    p1.setHand([1,3,4,5,6,7,8,9,10,12])
    r4 = p1.phasesFullfilled()
    if r4 == {4,5}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r4}\nExpected phases 4 and 5")

    print("\nTest run of 7:")
    p1.setHand([1,4,5,6,7,8,9,10,12,12])
    r5 = p1.phasesFullfilled()
    if r5 == {4}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r5}\nExpected phase 4")

    print("\nTest run of 7 (just under):")
    p1.setHand([1,2,5,6,7,8,9,10,12,12])
    r6 = p1.phasesFullfilled()
    if not r6:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r6}\nExpected no phases")

    # Test sets
    print("\nTest 2 sets of 3:")
    p1.setHand([1,1,1,6,7,8,10,12,12,12])
    r7 = p1.phasesFullfilled()
    if r7 == {1}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r7}\nExpected phase 1")

    print("\nTest 2 sets of 4:")
    p1.setHand([1,1,1,1,7,8,12,12,12,12])
    r8 = p1.phasesFullfilled()
    if r8 == {1,7}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r8}\nExpected phases 1 and 7")

    print("\nTest 1 set of 5 + 1 set of 2:")
    p1.setHand([1,1,1,1,1,8,9,11,12,12])
    r9 = p1.phasesFullfilled()
    if r9 == {9}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r9}\nExpected phase 9")

    print("\nTest 1 set of 5 + 1 set of 3:")
    p1.setHand([1,1,1,1,1,8,9,12,12,12])
    r10 = p1.phasesFullfilled()
    if r10 == {1, 9, 10}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r10}\nExpected phases 1, 9, and 10")

    print("\nTest 1 set of 5 + 1 set of 3 (with 4):")
    p1.setHand([1,1,1,1,1,8,12,12,12,12])
    r11 = p1.phasesFullfilled()
    if r11 == {1, 7, 9, 10}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r11}\nExpected phases 1, 7, 9, and 10")

    print("\nTest 1 set of 5 + 1 set of 3 (with 5):")
    p1.setHand([1,1,1,1,1,8,12,12,12,12])
    r12 = p1.phasesFullfilled()
    if r12 == {1, 7, 9, 10}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r12}\nExpected phases 1, 7, 9, and 10")

    # Test phases 2 and 3
    print("\nTest 1 set of 3 + 1 run of 4:")
    p1.setHand([1,1,5,6,7,8,10,10,10,12])
    r13 = p1.phasesFullfilled()
    if r13 == {2}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r13}\nExpected phase 2")

    print("\nTest 1 set of 3 + 1 run of 4(run with set in middle (fail)):")
    p1.setHand([1,1,5,6,7,8,7,7,10,12])
    r14 = p1.phasesFullfilled()
    if not r14:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r14}\nExpected zero phases")

    print("\nTest 1 set of 3 + 1 run of 4(run with set in middle (success)):")
    p1.setHand([3,4,5,6,7,8,7,7,10,12])
    r15 = p1.phasesFullfilled()
    if r15 == {2}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r15}\nExpected phase 2")

    print("\nTest 1 set of 4 + 1 run of 4:")
    p1.setHand([1,1,5,6,7,8,10,10,10,10])
    r16 = p1.phasesFullfilled()
    if r16 == {2,3}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r16}\nExpected phases 2 and 3")

    print("\nTest 1 set of 4 + 1 run of 4(run with set in middle (fail)):")
    p1.setHand([1,1,5,6,7,8,7,7,7,12])
    r17 = p1.phasesFullfilled()
    if r17 == {2}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r17}\nExpected phase 2")

    print("\nTest 1 set of 4 + 1 run of 4(run with set in middle (success)):")
    p1.setHand([3,4,5,6,7,8,7,7,7,12])
    r18 = p1.phasesFullfilled()
    if r18 == {2,3}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r18}\nExpected phases 2 and 3")

    # Test combined phases (where we try to shove as much as possible inside)
    print("\nTest run of 8 and set of 3 (run of 4) combo:")
    p1.setHand([3,4,5,6,7,8,9,10,10,10])
    r19 = p1.phasesFullfilled()
    if r19 == {2,4,5}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r19}\nExpected phases 2, 4, and 5")

    print("\nTest run of 7 and set of 3 (run of 4) combo:")
    p1.setHand([1,4,5,6,7,8,9,10,10,10])
    r20 = p1.phasesFullfilled()
    if r20 == {2,4}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r20}\nExpected phases 2 and 4")

    print("\nTest run of 7 and set of 4 (run of 4) combo:")
    p1.setHand([4,5,6,7,8,9,10,10,10,10])
    r20 = p1.phasesFullfilled()
    if r20 == {2,3,4}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r20}\nExpected phases 2, 3, and 4")

    print("\nTest 2 sets of 3 + run of 4 combo:")
    p1.setHand([1,1,1,2,2,2,3,4,5,6])
    r21 = p1.phasesFullfilled()
    if r21 == {1,2}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r21}\nExpected phases 1 and 2")

    print("\nTest 2 sets of 4 + run of 4 combo:")
    p1.setHand([1,1,1,1,2,2,2,2,3,4])
    r22 = p1.phasesFullfilled()
    if r22 == {1,2,7}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r22}\nExpected phases 1, 2, and 7")

    print("\nTest 6 of one card")
    p1.setHand([1,1,1,1,1,1,2,3,4,5])
    r23 = p1.phasesFullfilled()
    if r23 == {1,2,3}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r23}\nExpected phases 1, 2, and 3")

    print("\nTest 6 of one card (and 4 of another)")
    p1.setHand([1,1,1,1,1,1,2,2,2,2])
    r24 = p1.phasesFullfilled()
    if r24 == {1,7,9,10}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r24}\nExpected phases 1, 7, 9, and 10")

    print("\nTest 7 of one card")
    p1.setHand([1,1,1,1,1,1,1,2,3,4])
    r25 = p1.phasesFullfilled()
    if r25 == {1,2,3,9}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r25}\nExpected phases 1, 2, 3, and 9")

    print("\nTest 8 of one card")
    p1.setHand([1,1,1,1,1,1,1,1,2,3])
    r26 = p1.phasesFullfilled()
    if r26 == {1,7,9,10}:
        print("PASSED")
    else:
        testsFailed = True
        print(f"FAILED: Found the following phases: {r26}\nExpected phases 1, 7, 9, and 10")

    if testsFailed:
        print("\nFAILED: At least one test failed. Please look back to find failed test.")
    else:
        print("\nPASSED: All tests passed! Congratulations!")

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--test', action='store_true',
                        help='Run automated tests')
    args = vars(parser.parse_args(sys.argv[1:]))
    # print(args)
    if args['test']:
        print("---------Starting tests---------")
        test(args)
    else:
        main(args)
