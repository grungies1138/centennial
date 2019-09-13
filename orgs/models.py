from __future__ import unicode_literals

from django.db import models


"""
Functions of the Org class:

Initialize: new Org created
add members
remove members
add leaders
remove leaders
add credits
remove credits
add resources
remove resources
add assets
remove assets
add child orgs
remove child orgs
set active
set inactive
set motd
set headquarters
add branches
remove branches
set description
make hidden
make visible
"""


class Org(models.Model):
    # Org Name
    db_key = models.CharField(max_length=50, db_index=True)

    # list of members in the org
    db_members = models.ManyToManyField("OrgMember", null=True, related_name='members')

    # List of leaders with added permissions
    db_leaders = models.ManyToManyField("OrgMember", null=True, related_name='leaders')

    # number of credits in the org's account
    db_credits = models.BigIntegerField(default=0)

    # Amount of resources available to the org
    db_resources = models.BigIntegerField(default=0)

    # List of 'hard' assets.  (i.e. Ships, vehicles, armies)
    db_assets = models.ManyToManyField("objects.ObjectDB", null=True)

    # list of child orgs within the org
    db_child_orgs = models.ManyToManyField("Org", null=True)

    # Is this org active and able to receive members?
    db_active = models.BooleanField(default=True)

    # Message of the Day to be displayed to members on connect
    db_motd = models.TextField()

    # list of potential members that need to be reviewed and accepted or rejected.
    db_pending = models.ManyToManyField("objects.ObjectDB", null=True)

    # Reference to the parent org, if any
    db_parent = models.ForeignKey("Org", on_delete=models.CASCADE, null=True)

    # db_start = models.BooleanField()
    db_headquarters = models.ForeignKey("objects.ObjectDB", null=True)  # Reference to the org's headquarters

    # References to any branches set up in different zones.
    db_branches = models.ManyToManyField("objects.ObjectDB", null=True)

    # Description of the org
    db_desc = models.CharField(max_length=250)

    # Is org hidden from public View Orgs
    db_hidden = models.BooleanField(default=False)

    def __init__(self, name):
        self.db_key = name

    def add_member(self, member):
        self.db_members.add(member)

    def remove_member(self, member):
        self.db_members.remove(member)

    def get_members(self):
        return self.db_members.all()

    def get_member(self, name):
        pass

    def add_leader(self, leader):
        pass

    def remove_leader(self, leader):
        pass

    def add_credits(self, amount):
        pass

    def remove_credits(self, amount):
        pass

    def add_resources(self, amount):
        pass

    def remove_resources(self, amount):
        pass

    def add_asset(self, asset):
        pass

    def remove_asset(self, asset):
        pass

    def add_child_org(self, org):
        pass

    def remove_child_org(self, org):
        pass

    def toggle_active(self):
        pass

    def toggle_hidden(self):
        pass

    def set_motd(self, text):
        pass

    def set_hq(self, hq):
        pass

    def add_branch(self, branch):
        pass

    def remove_branch(self, branch):
        pass

    @property
    def description(self):
        pass


"""
Org Member class functions

Initialize
set rank
set assignment
assign assets
pay
"""


class OrgMember(models.Model):
    db_member = models.ForeignKey("objects.ObjectDB", null=True, on_delete=models.CASCADE)
    db_rank = models.CharField(max_length=50, null=True)
    db_assignment = models.CharField(max_length=50, null=True)
    db_assigned_assets = models.ManyToManyField("objects.ObjectDB", null=True)
    db_org = models.ForeignKey("Org", on_delete=models.CASCADE)
    db_pay = models.BigIntegerField(default=0)
