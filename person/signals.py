__author__ = 'shantya'
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete


def test_post_save_signal(sender, instance, *args, **kwargs):
    print sender
    print instance


pre_delete.connect(test_post_save_signal, sender=User)