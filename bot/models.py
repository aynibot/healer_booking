from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Create your models here.
class Basis(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Member(Basis):
    line_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=64, default='')
    photo = models.URLField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name