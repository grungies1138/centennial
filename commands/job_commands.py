from evennia import default_cmds
from evennia.utils.evmenu import EvMenu
from jobs.models import Bucket, Job, Roll, JobMessage
from evennia.utils import evtable
from commands.library import titlecase, notify
import datetime
import sys


class AddJobCommand(default_cmds.MuxCommand):
    """
        This allows players to enter in
        special requests that require staff attention as well as bug
        reports and other technical issues.
    Usage:
        +jobs
    """

    key = "+jobs"
    aliases = ["jobs"]
    lock = "cmd:perm(Player)"
    help_category = "General"

    def func(self):
        EvMenu(self.caller, "commands.job_commands",
               startnode="menu_start_node",
               node_formatter=node_formatter,
               options_formatter=options_formatter,
               cmd_on_exit=exit_message)


def menu_start_node(caller):
    text = "Welcome to the Jobs system menu.  Please make a selection from the list below to begin."

    options = ()

    if caller.locks.check_lockstring(caller, "dummy:perm(Admin)"):
        new_jobs = Job.objects.filter(db_status__in=['N']).filter(db_viewers__in=[caller])
        options += ({"desc": "View open jobs (%s)" % len(new_jobs),
                                "goto": "jobs_start"},
                             {"desc": "Add a new Job",
                              "goto": "add_job"},
                             {"desc": "Administration",
                              "goto": "admin_start"},)
    else:
        new_jobs = Job.objects.filter(db_status__in=['N']).filter(db_viewers__in=[caller])
        options += ({"desc": "View open jobs (%s)" % len(new_jobs),
                              "goto": "jobs_start"},
                             {"desc": "Add a new Job",
                              "goto": "add_job"})

    return text, options


def admin_start(caller):
    text = "Please select the Administrative function you wish to work with."
    new_jobs = Job.objects.filter(db_status__in=['N'])
    options = ({"desc": "Buckets",
                "goto": "buckets_start"},
               {"desc": "Jobs (%s New)" % len(new_jobs),
                "goto": "admin_jobs_start"},
               {"desc": "Go Back",
                "goto": "menu_start_node"})

    return text, options


#   JOBS  #######################
def admin_jobs_start(caller):
    jobs = None
    table = None
    jobs = Job.objects.all().exclude(db_status__in=['C'])
    table = evtable.EvTable("ID", "Job Summary", "Msgs", "Rolls", "Opened By:", "Opened", "Stat",
                            border="header", header_line_char='-')
    for job in jobs:
        table.add_row(job.id, job.db_key[:20], job.db_messages.count(), job.db_rolls.count(),
                      job.db_viewers.all().first(), job.db_opened_date.strftime("%m/%d/%y %H:%M"), job.db_status)

    table.reformat_column(0, width=5)
    table.reformat_column(1, width=20)
    table.reformat_column(2, width=6, align='r')
    table.reformat_column(3, width=7, align='r')
    table.reformat_column(4, width=18)
    table.reformat_column(5, width=16)
    table.reformat_column(6, width=6)

    text = str(table) + "\n\nPlease enter the ID of the job you would like to view."

    options = ({"key": "_default",
                "exec": _set_admin_view_job,
                "goto": "admin_view_job"},
               {"desc": "Done",
                "key": "done",
                "goto": "admin_start"})

    return text, options


def _set_admin_view_job(caller, caller_input):
    input = caller_input.strip()
    selected_job = Job.objects.exclude(db_status__in=['C']).filter(id=input)
    setattr(caller.ndb._menutree, 'selected_job', selected_job)


def admin_view_job(caller):
    selected_job = caller.ndb._menutree.selected_job.first()
    if selected_job:
        text = '{wJob Summary:{n %s \n{wAssigned To:{n %s\n{wStatus:{n %s\n{wBucket:{n %s\n' % \
               (selected_job.db_key, selected_job.db_assigned_to.first(), selected_job.db_status,
                selected_job.db_bucket.db_key)
        for message in selected_job.db_messages.all():
            text += "-" * 78 + "\nSender: %s   Date Sent: %s \n\n%s\n\n" % \
                               (message.db_sender.all().first(), message.db_date_sent.strftime("%m/%d/%y %H:%M"),
                                message.db_message)

        if selected_job.db_rolls.count() > 0:
            text += "Rolls".center(78, "-")
            for roll in selected_job.db_rolls.all():
                text += "%s - %s: %s" % (roll.db_sender.all().first(), roll.db_skill, roll.db_roll)

        options = ({"desc": "Add Comment",
                    "goto": "admin_job_add_message"},
                   {"desc": "Change Status",
                    "goto": "admin_job_status"},
                   {"desc": "Assign",
                    "goto": "ask_admin_assign_job"},
                   {"desc": "Go Back",
                    "goto": "admin_jobs_start"})

        return text, options
    else:
        text = "Invalid Job."
        options = ({"desc": "Go Back",
                    "goto": "jobs_start"})
        return text, options


def ask_admin_assign_job(caller):
    text = "Please enter the name of the staff member you wish to assign this job to."

    options = ({"key": "_default",
                "exec": _set_admin_assign_job,
                "goto": "admin_view_job"},
               {"desc": "Cancel",
                "key": "cancel",
                "goto": "admin_view_job"})

    return text, options


def _set_admin_assign_job(caller, caller_input):
    selected_job = caller.ndb._menutree.selected_job.first()
    assignee = caller.search(caller_input.strip())
    if assignee and caller.locks.check_lockstring(assignee, "dummy:perm(Helper)"):
        selected_job.db_assigned_to.add(assignee)
    else:
        caller.msg("That user either does not exist or does not have appropriate permissions to accept job assignments.")


def admin_job_status(caller):
    selected_job = caller.ndb._menutree.selected_job.first()
    text = "Current Job Status: %s\n\nPlease select the status you wish to change the job to." \
           % parse_status(selected_job.db_status)

    options = ({"desc": "New",
                "exec": lambda caller: selected_job.set_status("N"),
                "goto": "admin_jobs_start"},
               {"desc": "In Progress",
                "exec": lambda caller: selected_job.set_status("I"),
                "goto": "admin_jobs_start"},
               {"desc": "On Hold",
                "exec": lambda caller: selected_job.set_status("H"),
                "goto": "admin_jobs_start"},
               {"desc": "Waiting",
                "exec": lambda caller: selected_job.set_status("W"),
                "goto": "admin_jobs_start"},
               {"desc": "Closed",
                "exec": lambda caller: selected_job.set_status("C"),
                "goto": "admin_jobs_start"})

    return text, options


def admin_job_add_message(caller):
    text = "Enter the message that you wish to add to the Job"

    options = ({"key": "_default",
                "exec": _set_job_add_message,
                "goto": "admin_view_job"},
               {"desc": "Cancel",
                "goto": "view_job"})
    return text, options


def jobs_start(caller):
    jobs = None
    table = None
    jobs = Job.objects.filter(db_viewers__in=[caller]).exclude(db_status__in=['C'])
    table = evtable.EvTable("ID", "Job Summary", "Msgs", "Rolls", "Assigned To", "Opened", "Stat",
                            border="header", header_line_char='-')
    for job in jobs:
        table.add_row(job.id,job.db_key[:20], job.db_messages.count(), job.db_rolls.count(),
                      job.db_assigned_to.all().first(),job.db_opened_date.strftime("%m/%d/%y %H:%M"), job.db_status)

    table.reformat_column(0, width=5)
    table.reformat_column(1, width=20)
    table.reformat_column(2, width=6, align='r')
    table.reformat_column(3, width=7, align='r')
    table.reformat_column(4, width=18)
    table.reformat_column(5, width=16)
    table.reformat_column(6, width=6)

    text = str(table) + "\n\nPlease enter the ID of the job you would like to view."

    options = ({"key": "_default",
                "exec": _set_view_job,
                "goto": "view_job"},
               {"desc": "Done",
                "key": "done",
                "goto": "menu_start_node"})

    return text, options


def add_job(caller):
    table = evtable.EvTable("ID","Name", "Description", border="header", header_line_char='-')
    bucket_list = Bucket.objects.all()
    for bucket in bucket_list:
        table.add_row(bucket.id,bucket.db_key, bucket.db_description)

    table.reformat_column(0, width=6, valign="t", pad_bottom=1)
    table.reformat_column(1, width=25, valign="t", pad_bottom=1)
    table.reformat_column(2, width=40, valign="t", pad_bottom=1)

    text = str(table) + "\n\nSelect the ID of the Bucket you wish to add your job to."

    options = ({"key": "_default",
                "exec": _set_job_bucket,
                "goto": "ask_job_summary"},
               {"desc": "Cancel",
                "key": "cancel",
                "goto": "jobs_start"})

    return text, options


def _set_job_bucket(caller, caller_input):
    job_bucket = Bucket.objects.filter(id=caller_input.strip()).first()
    setattr(caller.ndb._menutree, "job_bucket", job_bucket)


def ask_job_summary(caller):
    job_bucket = caller.ndb._menutree.job_bucket

    if job_bucket:
        text = "Please enter a summary for the reason for this job.  Please note, there is a 50 character limit.  " \
               "Summaries longer than 50 characters will be truncated."

        options = ({"key": "_default",
                    "exec": _set_job_summary,
                    "goto": "ask_job_message"})

        return text, options
    else:
        text = "Invalid Bucket."
        options = ({"desc": "Go Back",
                    "goto": "add_job"})
        return text, options


def _set_job_summary(caller, caller_input):
    trunc_input = caller_input.strip()[:50]
    setattr(caller.ndb._menutree, "job_summary", trunc_input)


def ask_job_message(caller):
    text = "Please enter the issue you are having or what message you want to convey."

    options = ({"key": "_default",
                "exec": _set_job_message,
                "goto": "confirm_job"})
    return text, options


def _set_job_message(caller, caller_input):
    setattr(caller.ndb._menutree, "job_message", caller_input.strip())


def confirm_job(caller):
    text = "Bucket: %s\nJob Summary: %s\nMessage: %s\n\nPlease review the material above to ensure it is accurate.  " \
           "If yes, then the job will be created.  No will redirect you back to the main menu." % \
           (caller.ndb._menutree.job_bucket.db_key, caller.ndb._menutree.job_summary, caller.ndb._menutree.job_message)

    options = ({"desc": "Yes",
                "key": ("Y", "y", "Yes", "yes"),
                "exec": _create_job,
                "goto": "menu_start_node"},
               {"desc": "No",
                "key": ("N", "n", "No", "no"),
                "goto": "menu_start_node"})

    return text, options


def _create_job(caller):
    try:
        bucket = caller.ndb._menutree.job_bucket
        new_job = Job.objects.create(db_bucket=caller.ndb._menutree.job_bucket,
                                     db_key=caller.ndb._menutree.job_summary,
                                     db_status='N',
                                     db_opened_date=datetime.datetime.now())
        new_job.db_viewers.add(caller)
        new_job.locks.add("examine:id(%s);view:perm(PlayerHelpers)" % caller.id)
        new_message = JobMessage.objects.create(db_job=new_job,
                                                db_date_sent=datetime.datetime.now(),
                                                db_message=caller.ndb._menutree.job_message)
        new_message.db_sender.add(caller)

        new_job.db_messages.add(new_message)

        bucket.db_jobs.add(new_job)
        notify(caller, "dummy:perm(Builder)", "Job %s created by %s" %
               (new_job.id, new_job.db_viewers.first().key))
    except:
        caller.msg(sys.exc_info()[0])


def _set_view_job(caller, caller_input):
    input = caller_input.strip()
    selected_job = Job.objects.filter(db_viewers__in=[caller]).exclude(db_status__in=['C']).filter(id=input)
    setattr(caller.ndb._menutree, 'selected_job', selected_job)


def view_job(caller):
    selected_job = caller.ndb._menutree.selected_job.first()
    if selected_job:
        text = '{wJob Summary:{n %s \n{wAssigned To:{n %s\n{wStatus:{n %s\n{wBucket:{n %s\n' % \
            (selected_job.db_key, selected_job.db_assigned_to.first(), parse_status(selected_job.db_status), selected_job.db_bucket.db_key)
        for message in selected_job.db_messages.all():
            text += "-" * 78 + "\nSender: %s   Date Sent: %s \n\n%s\n\n" % \
                               (message.db_sender.all().first(), message.db_date_sent.strftime("%m/%d/%y %H:%M"),
                                message.db_message)

        if selected_job.db_rolls.count() > 0:
            text += "Rolls".center(78, "-")
            for roll in selected_job.db_rolls.all():
                text += "%s - %s: %s" % (roll.db_sender.all().first(), roll.db_skill, roll.db_roll)

        options = ({"desc": "Add Comment",
                    "goto": "job_add_message"},
                   {"desc": "Add Roll",
                    "goto": "job_add_roll"},
                   {"desc": "Close Job",
                    "exec": lambda caller: selected_job.set_status('C'),
                    "goto": "jobs_start"},
                   {"desc": "Go Back",
                    "goto": "jobs_start"})

        return text, options
    else:
        text = "Invalid Job."
        options = ({"desc": "Go Back",
                    "goto": "jobs_start"})
        return text, options


def job_add_roll(caller):
    text = "Not yet implemented."
    options = ({"desc": "Go Back",
                "goto": "view_job"})
    return text, options


def job_add_message(caller):
    text = "Enter the message that you wish to add to the Job"

    options = ({"key": "_default",
                "exec": _set_job_add_message,
                "goto": "view_job"},
               {"desc": "Cancel",
                "goto": "view_job"})

    return text, options


def _set_job_add_message(caller, caller_input):
    selected_job = caller.ndb._menutree.selected_job.first()
    new_message = JobMessage.objects.create(db_job=selected_job,
                                            db_date_sent=datetime.datetime.now(),
                                            db_message=caller_input)
    new_message.db_sender.add(caller)
    selected_job.db_messages.add(new_message)
    caller.msg(str(selected_job.db_messages.first().db_sender.first()))
    for owner in selected_job.db_viewers.all():
        notify(caller, "dummy:id(%s)" % owner.id, "Message added to Job %s by %s" % (selected_job.id, caller))

    notify(caller, "dummy:perm(Builder)", "Message added to Job %s by %s" % (selected_job.id, caller))


#  BUCKETS  #######################
def buckets_start(caller):
    text = "Please select the funciton you would like to do with Buckets."

    options = ({"desc": "View Buckets",
                "goto": "view_buckets"},
               {"desc": "Add a Bucket",
                "goto": "add_bucket"},
               {"desc": "Delete a Bucket",
                "goto": "delete_bucket"},
               {"desc": "Go Back",
                "goto": "admin_start"})

    return text, options


def delete_bucket(caller):
    table = evtable.EvTable("ID", "Name", "Jobs", "SLA", border="header", header_line_char='-')
    bucket_list = Bucket.objects.all()
    for bucket in bucket_list:
        table.add_row(bucket.id, bucket.db_key, bucket.db_jobs.count(), bucket.db_sla)

    table.reformat_column(0, width=25)
    table.reformat_column(1, width=25)
    table.reformat_column(2, width=6, align="r")
    table.reformat_column(3, width=5, align="r")

    text = str(table) + "\n\nEnter the ID of the Bucket you would like to delete. Or select Done to return to the " \
                        "previous menu.\n\n{rWARNING: Buckets with open jobs will not be deleted.{n"

    options = ({"key": "_default",
                "exec": attempt_bucket_delete,
                "goto": "delete_bucket"},
               {"desc": "Done",
                "key": "done",
                "goto": "buckets_start"})

    return text, options


def attempt_bucket_delete(caller, caller_input):
    input = int(caller_input.strip())
    if input:
        bucket_to_delete = Bucket.objects.filter(id=input).first()
        if bucket_to_delete.db_jobs and bucket_to_delete.db_jobs.exclude(db_status__in=['C']).count() > 0:
                caller.msg("{r*** WARNING ***{n You cannot delete a bucket with open jobs.  Close those jobs and try "
                           "again.")
        else:
            bucket_to_delete.delete()


def view_buckets(caller):
    table = evtable.EvTable("Name", "Description", "Jobs", "SLA", "Locks", border="header", header_line_char='-')
    bucket_list = Bucket.objects.all()

    for bucket in bucket_list:
        table.add_row(bucket.db_key, bucket.db_description, bucket.db_jobs.count(), bucket.db_sla, bucket.locks)

    table.reformat_column(0, width=25)
    table.reformat_column(1, width=25)
    table.reformat_column(2, width=6, align="r")
    table.reformat_column(3, width=5, align="r")
    table.reformat_column(4, width=10)

    text = table

    options = ({"desc": "Go Back",
                "goto": "buckets_start"})

    return text, options


#  Add Bucket
def add_bucket(caller):
    text = "Please enter the name of the Bucket you would like to create."

    options = ({"key": "_default",
                "exec": _set_bucket_name,
                "goto": "ask_bucket_description"},
               {"desc": "Cancel",
                "goto": "buckets_start"})

    return text, options


def _set_bucket_name(caller, caller_input):
    caller_input = caller_input.strip()
    setattr(caller.ndb._menutree, "bucket_name", caller_input)


def ask_bucket_description(caller):
    text = "Name: %s \n\nPlease enter the Bucket description." % caller.ndb._menutree.bucket_name

    options = ({"key": "_default",
                "exec": _set_bucket_desc,
                "goto": "ask_bucket_sla"},
               {"desc": "Cancel",
                "goto": "buckets_start",
                "exec": clear_bucket_create})

    return text, options


def _set_bucket_desc(caller, caller_input):
    caller_input = caller_input.strip()
    setattr(caller.ndb._menutree, "bucket_desc", caller_input)


def ask_bucket_sla(caller):
    text = "Name: %s \nDescription: %s\n\nPlease enter the Bucket's Service Level Agreement.  This is the " \
           "number of hours before the jobs in this bucket are considered overdue" \
           % (caller.ndb._menutree.bucket_name, caller.ndb._menutree.bucket_desc)

    options = ({"key": "_default",
                "exec": _set_bucket_sla,
                "goto": "ask_bucket_locks"},
               {"desc": "Cancel",
                "goto": "buckets_start",
                "exec": clear_bucket_create})
    return text, options


def _set_bucket_sla(caller, caller_input):
    caller_input = caller_input.strip()
    setattr(caller.ndb._menutree, "bucket_sla", caller_input)


def ask_bucket_locks(caller):
    text = "Name: %s \nDescription: %s\nSLA: %s\n\nPlease enter the lockstring you wish to secure this bucket with.  " \
           "For no locks type None." \
           % (caller.ndb._menutree.bucket_name, caller.ndb._menutree.bucket_desc, caller.ndb._menutree.bucket_sla)

    options = ({"key": "_default",
                "exec": _set_bucket_locks,
                "goto": "ask_bucket_confirm"},
               {"desc": "Cancel",
                "goto": "buckets_start",
                "exec": clear_bucket_create})
    return text, options


def _set_bucket_locks(caller, caller_input):
    caller_input = caller_input.strip().lower()
    if "none" not in caller_input:
        setattr(caller.ndb._menutree, "bucket_locks", caller_input)
    else:
        setattr(caller.ndb._menutree, "bucket_locks", "")


def ask_bucket_confirm(caller):
    text = "Name: %s \nDescription: %s\nSLA: %s\nLocks: %s\n\nPlease review the above information.  " \
           "If it is accurate, type Y to confirm and create your new bucket.  If not, type N and you will be" \
           "redirected back to the beginning and the bucket information will be cleared." \
           % (caller.ndb._menutree.bucket_name, caller.ndb._menutree.bucket_desc,
              caller.ndb._menutree.bucket_sla, caller.ndb._menutree.bucket_locks)

    options = ({"desc": "Yes",
                "key": "Y",
                "exec": create_bucket,
                "goto": "buckets_start"},
               {"desc": "No",
                "key": "N",
                "exec": clear_bucket_create,
                "goto": "buckets_start"})
    return text, options


def create_bucket(caller):
    new_bucket = Bucket.objects.create(db_key=caller.ndb._menutree.bucket_name,
                                       db_description=caller.ndb._menutree.bucket_desc,
                                       db_sla=int(caller.ndb._menutree.bucket_sla))
    if caller.ndb._menutree.bucket_locks:
        new_bucket.locks.add(caller.ndb._menutree.bucket_locks)
    notify(caller, "dummy:perm(Builder)", "Bucket %s has been created" % new_bucket.db_key)


def clear_bucket_create(caller):
    if caller.ndb._menutree.bucket_name:
        del caller.ndb._menutree.bucket_name
    if caller.ndb._menutree.bucket_desc:
        del caller.ndb._menutree.bucket_desc

    if caller.ndb._menutree.bucket_sla:
        del caller.ndb._menutree.bucket_sla
    if caller.ndb._menutree.bucket_locks:
        del caller.ndb._menutree.bucket_locks


#  UTILITY  #######################
def parse_status(abbr):
    if abbr == 'N':
        return "NEW"
    elif abbr == 'I':
        return "IN PROGRESS"
    elif abbr == 'H':
        return "ON HOLD"
    elif abbr == 'W':
        return "WAITING"
    elif abbr == 'C':
        return "CLOSED"


def node_formatter(nodetext, optionstext, caller=None):
    separator1 = "|010_|n" * 78 + "\n\n"
    separator2 = "\n" + "|010_|n" * 78 + "\n\n|330You may type '|540q|n' |330or|n '|540quit|n' " \
                                         "|330at any time to quit.|n\n" + "|010_|n" * 78 + "\n\n"
    return separator1 + nodetext + separator2 + optionstext


def options_formatter(optionlist, caller=None):
    options = []
    for key, option in optionlist:
        options.append("{w%s{n: %s" % (key, option))

    return "\n".join(options)


def exit_message(caller, menu):
    caller.msg("Exiting +jobs.  Goodbye.")
