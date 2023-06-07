import uuid
from django.db import models


class Language(models.Model):
    """A programming language"""
    title = models.CharField(max_length=100, blank=False, primary_key=True)
    color = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class GitRepo(models.Model):
    """Emulates a Git repository"""
    url = models.URLField(max_length=500, blank=False, primary_key=True)
    title = models.CharField(max_length=200, blank=False, default='')
    description = models.CharField(max_length=500, blank=False, default='')
    image = models.URLField(max_length=500, blank=False, default='')
    languages = models.ManyToManyField(
        Language, blank=True, related_name='repos')

    def __str__(self):
        return self.url


EDUCATION_STATE = (
    ("Completed", "COMPLETED"),
    ("In-progress", "IN_PROGRESS"),
    ("Not-started", "NOT_STARTED"),
)


class Education(models.Model):
    """A model for an education"""
    title = models.CharField(max_length=200, blank=False, default='')
    description = models.CharField(max_length=500, blank=False, default='')
    url = models.URLField(max_length=500, blank=True, default='')
    image = models.URLField(max_length=500, blank=False, default='')
    state = models.CharField(choices=EDUCATION_STATE, max_length=100)
    certificate = models.URLField(max_length=500, blank=True, default='')
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title
