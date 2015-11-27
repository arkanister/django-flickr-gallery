from django.db import models


class Article(models.Model):
    """
    Article to test ckeditor
    """
    title = models.CharField(max_length=60)
    content = models.TextField()
