from django.db import models
from django.utils.text import Truncator
from django.core.validators import MaxValueValidator, MinValueValidator
from math import log, floor

class Investor(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children',on_delete=models.DO_NOTHING)
    innocence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    experience = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    charisma = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    money = models.FloatField()

    def GetProbabilityToFindInvestors(self):
        return self.experience * self.charisma * (1 - log(len(self.children_set),10))

    def GetProbabilityCandidateAccepts(self):
        return self.innocence * (1-self.experience)

    def GetMaximumWeeksWithoutRecovery(self):
        return floor(1 - self.innocence) * self.experience * self.charisma * 10
