from django import template
from django.db import models
# ? allows us to remove unwanted characters
from django.utils.text import slugify
from django.urls import reverse


import misaka  # allows us to do link inbedding

from django.contrib.auth import get_user_model  # ? Returns the user model
User = get_user_model()  # ? allows us to call things off of the current user session

register = template.Library()  # ? allows us to use custome template tags


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    # * methods
    def __str__(self):
        return self.name  # ? String representation is just going to be the group name

    #! To save a group
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = ['name']

    pass


# ? related_name - the group member is related to the group class through the foreign key which we have called memberships
class GroupMember(models.Model):
    # * Links
    group = models.ForeignKey(
        Group,
        related_name='memberships',
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        related_name='user_groups',
        on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username  # ? the string representation of the user

    class Meta:
        unique_together = ('group', 'user')
