from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Org(models.Model):
    db_key = models.CharField(max_length=50, db_index=True)  # Org Name
    db_members = models.ManyToManyField("OrgMember", null=True, related_name='members')  # list of members in the org
    db_leaders = models.ManyToManyField("OrgMember", null=True, related_name='leaders')  # List of leaders with added permissions
    db_credits = models.BigIntegerField(default=0)  # number of credits in the org's account
    db_resources = models.BigIntegerField(default=0)  # Amount of resources available to the org
    db_assets = models.ManyToManyField("objects.ObjectDB", null=True)  # List of 'hard' assets.  (i.e. Ships, vehicles, armies)
    db_child_orgs = models.ManyToManyField("Org", null=True)  # list of child orgs within the org
    db_active = models.BooleanField()  # Is this org active and able to receive members?
    db_motd = models.TextField()  # Message of the Day to be displayed to members on connect
    db_pending = models.ManyToManyField("objects.ObjectDB", null=True)  # list of potential members that need to be reviewed and accepted or rejected.
    db_parent = models.ForeignKey("Org", on_delete=models.CASCADE, null=True)  # Reference to the parent org, if any
    # db_start = models.BooleanField()
    db_headquarters = models.ForeignKey("objects.ObjectDB", null=True)  # Reference to the org's headquarters
    db_branches = models.ManyToManyField("objects.ObjectDB", null=True) # References to any branches set up in different zones.
    db_desc = models.CharField(max_length=250)  # Description of the org
    db_hidden = models.BooleanField()


class OrgMember(models.Model):
    db_member = models.ForeignKey("objects.ObjectDB", null=True)
    db_rank = models.CharField(max_length=50, null=True)
    db_assignment = models.CharField(max_length=50, null=True)
    db_assigned_assets = models.ManyToManyField("objects.ObjectDB", null=True)
    db_org = models.ForeignKey("Org", on_delete=models.CASCADE)
