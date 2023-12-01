raise NotImplementedError(
    "This module is for sample code only. It is not intended to be executed."
)

from django.db import models


class Article(models.Model):
    written_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )  # should be fixable
