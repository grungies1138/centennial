from django.db import models
from evennia.utils.idmapper.models import SharedMemoryModel
from evennia.locks.lockhandler import LockHandler
from evennia.utils.utils import lazy_property


class Board(models.Model):
    db_key = models.CharField(max_length=35, db_index=True)
    db_timeout = models.IntegerField(null=True)
    lock_storage = models.TextField(null=True)
    db_description = models.TextField()
    db_members = models.ManyToManyField("objects.ObjectDB")
    db_posts = models.ManyToManyField("Post")


    @lazy_property
    def locks(self):
        return LockHandler(self)

    def access(self, accessing_obj, access_type='read', default=False):
        """
        Checks lock access.
        Args:
            accessing_obj (Object or Player): The object trying to gain access.
            access_type (str, optional): The type of lock access to check.
            default (bool): Fallback to use if `access_type` lock is not defined.
        Returns:
            result (bool): If access was granted or not.
        """
        return self.locks.check(accessing_obj,
                                access_type=access_type, default=default)


class Post(models.Model):
    db_key = models.CharField(max_length=35, db_index=True)
    db_message = models.TextField()
    db_sender = models.CharField(max_length=50)
    db_likes = models.IntegerField()
    db_has_liked = models.ManyToManyField("objects.ObjectDB", null=True)
    db_has_read = models.ManyToManyField("objects.ObjectDB", null=True)
    db_date_posted = models.DateField()
    db_comments = models.ManyToManyField("Comment", null=True)


class Comment(models.Model):
    db_author = models.CharField(max_length=50)
    db_message = models.TextField()
    db_likes = models.IntegerField()
    db_date_posted = models.DateField()
    db_has_liked = models.ManyToManyField("objects.ObjectDB", null=True)
