from django.db import models


class Language(models.Model):
    """A programming language"""
    title = models.CharField(max_length=100, blank=False, primary_key=True)
    color = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class GitRepo(models.Model):
    """Emulates a Git repository"""
    url = models.URLField(blank=False, primary_key=True)
    title = models.CharField(max_length=100, blank=False, default='')
    description = models.CharField(max_length=500, blank=False, default='')
    image = models.URLField(blank=False, default='')
    languages = models.ManyToManyField(
        Language, blank=True, related_name='repos')

    def __str__(self):
        return self.url
