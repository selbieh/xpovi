from django.contrib.auth.models import User
from django.db import models

from base.models import BaseModel


class QuestionSection(BaseModel):
    order = models.IntegerField(default=0.)
    title = models.CharField(null=True, blank=True, max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.title or self.id


class Question(BaseModel):
    question = models.CharField(null=False, blank=False, default='', max_length=255)
    section = models.ForeignKey(QuestionSection, null=False, on_delete=models.PROTECT,
                                related_name='questions')

    def __str__(self):
        return self.question


class Answer(BaseModel):
    answer = models.CharField(null=False, blank=False, default='', max_length=255)
    question = models.ForeignKey(Question, null=False, on_delete=models.PROTECT, related_name='answers')

    def __str__(self):
        return self.answer


class UserSectionAnswers(BaseModel):
    CONFIRMED = "confirmed"
    INIT = 'init'
    answer_state_choices = [
        (CONFIRMED, CONFIRMED),
        (INIT, INIT)
    ]
    status = models.CharField(max_length=15, default=INIT, choices=answer_state_choices)
    section = models.ForeignKey(QuestionSection, on_delete=models.PROTECT, null=False, blank=False)
    answers = models.ManyToManyField(Answer, blank=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)
