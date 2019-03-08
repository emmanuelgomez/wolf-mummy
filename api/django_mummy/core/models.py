from django.db import models
from django.utils.text import Truncator
from django.core.validators import MaxValueValidator, MinValueValidator
from math import log, floor

class Investor(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children',on_delete=models.CASCADE)
    innocence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    experience = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    charisma = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    money = models.FloatField()
    is_mummy = models.BooleanField()
    week = models.IntegerField()

    def GetChildrens(self):
        return self.children.all()

    def GetProbabilityToFindInvestors(self):
        if len(self.children.all()) == 0:
            maxChildrenPenalty = 0
        else:maxChildrenPenalty=log(len(self.children.all()),10)
        return self.experience * self.charisma * (1 - maxChildrenPenalty )

    def GetProbabilityCandidateAccepts(self):
        return self.innocence * (1-self.experience)

    def MemberIsLeavingProgram(self):
        return self.week < (floor(1 - self.innocence) * self.experience * self.charisma * 10)
