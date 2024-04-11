from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=10)
    # поменять тип
    phone = models.CharField(max_length=10)
    devices = models.ManyToManyField('Device', related_name='users')

    def __str__(self):
        return self.name


class Device(models.Model):
    # подумала, что с простым id помимо uuid будет проще, не факт
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=12)
    name = models.CharField(max_length=40)
    type = models.CharField(max_length=40)

    def __str__(self):
        return self.name
