from django.db import models

class Blogpage(models.Model):
    message = models.CharField(max_length=250)

