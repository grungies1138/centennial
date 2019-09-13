from django.db import models
from evennia.locks.lockhandler import LockHandler
from evennia.utils.utils import lazy_property


class Bucket(models.Model):
    db_key = models.CharField(max_length=25, db_index=True)
    db_description = models.TextField()
    db_jobs = models.ManyToManyField("Job", null=True)
    db_sla = models.IntegerField()
    lock_storage = models.TextField(null=True)

    @lazy_property
    def locks(self):
        return LockHandler(self)


class Job(models.Model):

    JOB_STATUSES = (
        ('N', "NEW"),
        ('I', 'In Progress'),
        ('H', 'ON HOLD'),
        ('W', 'WAITING'),
        ('C', 'CLOSED')
    )
    db_bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    db_key = models.CharField(max_length=50, db_index=True)
    db_messages = models.ManyToManyField("JobMessage")
    db_rolls = models.ManyToManyField("Roll", null=True)
    db_assigned_to = models.ManyToManyField("objects.ObjectDB", null=True)
    db_status = models.CharField(max_length=1, choices=JOB_STATUSES)
    db_completed_date = models.DateTimeField(null=True)
    db_opened_date = models.DateTimeField()
    db_viewers = models.ManyToManyField("objects.ObjectDB")
    lock_storage = models.TextField()

    @lazy_property
    def locks(self):
        return LockHandler(self)

    def set_status(self, value):
        self.db_status = value
        self.save()


class Roll(models.Model):
    db_job = models.ForeignKey(Job, on_delete=models.CASCADE)
    db_roller = models.ManyToManyField("objects.ObjectDB")
    db_skill = models.CharField(max_length=50)
    db_roll = models.IntegerField()


class JobMessage(models.Model):
    db_job = models.ForeignKey(Job, on_delete=models.CASCADE)
    db_sender = models.ManyToManyField("objects.ObjectDB")
    db_date_sent = models.DateTimeField()
    db_message = models.TextField()
