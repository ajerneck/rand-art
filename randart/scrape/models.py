from django.db import models

class Article(models.Model):
    url = models.URLField()
    title = models.TextField()
    text = models.TextField()
    label = models.IntegerField(blank=True, null=True)

class Result(models.Model):
    article = models.ForeignKey(Article)
    learner = models.CharField(max_length=400)
    label = models.IntegerField()

