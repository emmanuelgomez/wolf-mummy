from .models import Investor
import random
import threading
import time
class Manager(threading.Thread):
    members_leaving = []

    def __init__(self):
        threading.Thread.__init__(self)

    def Start(self,mummy):
        w = threading.Thread(target=self.worker, args=(mummy,))
        w.setDaemon(True)
        w.start()

    def worker(self,tree):

        mummy = Investor.objects.select_related('parent').get(is_mummy=True)
        while len(mummy.children) > 0:
            self.IterateTree(tree)
            self.RemoveMembersLeaving()
            mummy = Investor.objects.select_related('parent').get(is_mummy=True)
        return

    def IterateTree(self, tree):

        nodeStack = []
        nodeStack.append(tree)
        while len(nodeStack) > 0 :
            print(len(nodeStack))
            # Pop the top item from stack and print it
            node = nodeStack.pop()
            if node.parent is not None:
                self.TryToRecruitCandidate(node)
            # Push right and left children of the popped node
            # to stack
            node.week += 1
            node.save()
            if node.MemberIsLeavingProgram() and node.parent is not None:
                self.members_leaving.append(node)

            for investor in Investor.objects.filter(parent=node.id):
                nodeStack.append(investor)

    def TryToRecruitCandidate(self, investor):
        can_recruit = random.random()
        if can_recruit > investor.GetProbabilityToFindInvestors():
            candidate = self.PickCandidate()
            if candidate is not None:
                candidate.parent = investor
                candidate.save()
                investor.money += 100
                investor.save()
                mummy = Investor.objects.all().get(is_mummy=True)
                mummy.money += 500
                mummy.save()

    def PickCandidate(self):
        can_accept = random.random()
        min_candidate = Investor.objects.all().filter(parent=None).order_by('-innocence')
        if len(min_candidate) == 0:
            return None
        if can_accept > min_candidate[0].GetProbabilityCandidateAccepts():
            return min_candidate[0]
        else:
            return None

    def RemoveMembersLeaving(self):
        for member in self.members_leaving:
            member.delete()

    def GetMembersLeaving(self):
        return self.members_leaving

    @staticmethod
    def GenerateInvestors(total):
        for x in range(0, total):
            investor = Investor(innocence=random.random(), experience=random.random(), charisma=random.random(),
                                is_mummy=False, money=0, week=0, parent=None)
            investor.save()

    @staticmethod
    def GenerateMummyInvestors(total, mummy):
        for x in range(0, total):
            investor = Investor(innocence=random.random(), experience=random.random(), charisma=random.random(),
                                is_mummy=False, money=0, week=0, parent=mummy)
            investor.save()
            mummy.money += total * 500
            mummy.save()
