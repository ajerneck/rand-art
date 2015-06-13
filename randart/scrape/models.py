from django.db import models

class Article(models.Model):
    url = models.URLField()
    title = models.TextField()
    text = models.TextField()
    testing = models.TextField()