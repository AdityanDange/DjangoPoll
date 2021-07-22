import datetime
from account.models import Account

from django.db import models
from django.utils import timezone
from django.contrib import admin

class Question(models.Model):
    user = models.ForeignKey('account.Account', on_delete=models.CASCADE,default=1)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    popularity = models.IntegerField(default=0)
    
    def user_can_vote(self, user):
        """ 
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(question=self)
        if qs.exists():
            return False
        return True

    def __str__(self):
        return self.question_text
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.question.question_text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'