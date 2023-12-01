raise NotImplementedError(
    "This module is for sample code only. It is not intended to be executed."
)

from django.db import models


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # should be fixable
    related_news = models.OneToOneField(
        "news.News", on_delete=models.CASCADE
    )  # should not be fixable, because it is a string
    title = models.CharField(max_length=128)  # should not be a problem
