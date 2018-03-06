from evennia import default_cmds, search_object
from evennia.utils.evmenu import EvMenu
from evennia.typeclasses.tags import Tag
from orgs.models import Org, OrgMember
from evennia.utils import evtable
from commands.library import titlecase, notify, node_formatter, options_formatter, exit_message
import evennia
import locale


class OrgCommand(default_cmds.MuxCommand):
    """
        System for managing, creating, joining and leaving organizations.
        Usage:
            +orgs
    """

    key = "+orgs"
    aliases = ["orgs"]
    lock = "cmd:perm(Player)"
    help_category = "General"

    def func(self):
        EvMenu(self.caller, "commands.org_commands",
               startnode="menu_start_node",
               node_formatter=node_formatter,
               options_formatter=options_formatter,
               cmd_on_exit=exit_message)


def menu_start_node(caller):
    text = "Welcome to the Organization system.  Please choose an option below to begin.  If you wish to join an " \
           "org, simply browse to it and the option will be available, if possible."

    options = ()
    if caller.locks.check_lockstring(caller, "dummy:perm(Admin)"):
        options = ({"desc": "View Orgs",
                    "goto": "admin_view_orgs"},
                   {"desc": "Setup New Org",
                    "goto": "admin_setup_org"},
                   {"desc": "Edit Org",
                    "goto": "admin_edit_orgs"},
                   {"desc": "Delete Org",
                    "goto": "admin_delete_orgs"})

    return text, options


#                  ADMINISTRATION  ###################
def admin_delete_orgs(caller):
    table = evtable.EvTable("#", "Name", "Leader", border="header", header_line_char='-')
    orgs = Org.objects.all()

    for org in orgs:
        leader = org.db_leaders.first().db_member
        temp_hq = search_object(org.db_headquarters)
        if bool(temp_hq) is True:
            hq = temp_hq[0]
        else:
            hq = None

        table.add_row(org.id, org.db_key, leader)

    table.reformat_column(0, width=5)
    table.reformat_column(1, width=25)
    table.reformat_column(2, width=25)

    text = table

    options = ({"key": "_default",
                "exec": admin_select_edit_org,
                "goto": "admin_confirm_delete_org"},
               {"desc": "Go Back",
                "key": "back",
                "goto": "menu_start_node"})

    return text, options


def admin_confirm_delete_org(caller):
    selected_org = caller.ndb._menutree.selected_org
    text = "Are you sure you want to delete %s?  This process cannot be undone." % selected_org.db_key

    options = ({"desc": "Yes",
                "exec": admin_complete_delete_org,
                "goto": "menu_start_node"},
               {"desc": "No",
                "exec": admin_clear_selected_org,
                "goto": "menu_start_node"})

    return text, options


def admin_complete_delete_org(caller, caller_input):
    selected_org = caller.ndb._menutree.selected_org
    Org.objects.filter(id=selected_org.id).delete()
    admin_clear_selected_org(caller, caller_input)


def admin_clear_selected_org(caller, caller_input):
    del caller.ndb._menutree.selected_org


def admin_edit_orgs(caller):
    table = evtable.EvTable("#", "Name", "Leader", border="header", header_line_char='-')
    orgs = Org.objects.all()

    for org in orgs:
        leader = org.db_leaders.first().db_member
        temp_hq = search_object(org.db_headquarters)
        if bool(temp_hq) is True:
            hq = temp_hq[0]
        else:
            hq = None

        table.add_row(org.id, org.db_key, leader)

    table.reformat_column(0, width=5)
    table.reformat_column(1, width=25)
    table.reformat_column(2, width=25)

    text = table

    options = ({"key": "_default",
                "exec": admin_select_edit_org,
                "goto": "admin_edit_selected_org"},
               {"desc": "Go Back",
                "key": "back",
                "goto": "menu_start_node"})

    return text, options


def admin_select_edit_org(caller, caller_input):
    input_org_id = caller_input.strip()
    org_id = int(input_org_id)
    selected_org = None
    if org_id:
        selected_org = Org.objects.filter(id=org_id).first()

    if selected_org:
        setattr(caller.ndb._menutree, "selected_org", selected_org)
    else:
        caller.msg("|rError: Not a valid org.  Please review the org list and try again.")


def admin_edit_selected_org(caller):
    selected_org = caller.ndb._menutree.selected_org
    text = "Org: %s\n\n" % selected_org.db_key

    leaders = selected_org.db_leaders.all()
    leader_string = ""
    index = 0
    for leader in leaders:
        if index < len(leaders) - 1:
            leader_string += leader.db_member.name + ", "
        else:
            leader_string += leader.db_member.name
        index += 1

    text += "\nLeaders: %s" % leader_string

    members = selected_org.db_members.all()
    member_string = ""
    index = 0
    for member in members:
        if index < len(members) - 1:
            member_string += member.db_member.name + ", "
        else:
            member_string += member.db_member.name
        index += 1

    text += "\nMembers: %s" % member_string

    text += "\nCredits: {:,.0f}".format(selected_org.db_credits)

    text += "\nResources: {:,.0f}".format(selected_org.db_resources)

    assets = selected_org.db_assets.all()
    asset_string = ""
    index = 0
    for asset in assets:
        if index < len(assets):
            asset_string += asset.name + ", "
        else:
            asset_string += asset.name
        index += 1

    text += "\nAssets: %s" % asset_string

    if selected_org.db_active:
        status_text = "Active"
    else:
        status_text = "Inactive"

    text += "\nStatus: %s" % status_text

    text += "\nMessage of the Day: %s" % selected_org.db_motd

    text += "\nHeadquarters: %s" % selected_org.db_headquarters

    branches = selected_org.db_branches.all()
    branch_string = ""
    index = 0
    for branch in branches:
        if index < len(branches) - 1:
            branch_string += branch.name + ", "
        else:
            branch_string += branch.name
        index += 1

    text += "\nBranches: %s" % branch_string

    text += "\nDescription: %s" % selected_org.db_desc

    text += "\nHidden: %s" % selected_org.db_hidden

    options = ({"desc": "Edit Leaders",
                "goto": "admin_edit_leaders"},
               {"desc": "Edit Members",
                "goto": "admin_edit_members"},
               {"desc": "Edit Credits",
                "goto": "admin_edit_credits"},
               {"desc": "Edit Resources",
                "goto": "admin_edit_resources"},
               {"desc": "Edit Assets",
                "goto": "admin_edit_assets"},
               {"desc": "Edit Status",
                "goto": "admin_edit_status"},
               {"desc": "Edit MotD",
                "goto": "admin_edit_motd"},
               {"desc": "Edit Headquarters",
                "goto": "admin_edit_hq"},
               {"desc": "Edit Branches",
                "goto": "admin_edit_branches"},
               {"desc": "Edit Description",
                "goto": "admin_edit_desc"},
               {"desc": "Go Back",
                "goto": "menu_start_node"})

    return text, options


# ########### EDIT LEADERS ############################################

def admin_edit_leaders(caller):
    selected_org = caller.ndb._menutree.selected_org
    text = "Org: %s" % selected_org.db_key

    leaders = selected_org.db_leaders.all()
    leader_string = ""
    index = 0
    for leader in leaders:
        if index < len(leaders) - 1:
            leader_string += leader.db_member.name + ", "
        else:
            leader_string += leader.db_member.name
        index += 1

    text += "\n\nLeaders: %s" % leader_string

    options = ({"desc": "Add Leader",
                "goto": "admin_add_leader"},
               {"desc": "Remove Leader",
                "goto": "admin_remove_leader"},
               {"desc": "Go Back",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_add_leader(caller):
    text = "Type the name of the person you want to add as a leader for this Organization"

    options = ({"key": "_default",
                "exec": admin_set_add_leader,
                "goto": "admin_edit_selected_org"},
               {"desc": "Cancel",
                "key": "cancel",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_set_add_leader(caller, caller_input):
    selected_org = caller.ndb._menutree.selected_org
    temp_name = caller_input.strip()
    leader = search_object(temp_name)

    if leader:
        new_member = OrgMember.objects.create(db_org=selected_org)
        new_member.db_member = leader[0]
        new_member.save()

        selected_org.db_leaders.add(new_member)
        selected_org.save()
    else:
        caller.msg("|rError: Character not found.|n")


def admin_remove_leader(caller):
    selected_org = caller.ndb._menutree.selected_org
    text = "Below are listed the leaders for %s.  Please select the leader you wish to remove from the org." \
           % selected_org.db_key

    options = ()

    leaders = selected_org.db_leaders.all()

    for leader in leaders:
        node_dict = {"desc": leader.db_member.name, "goto": "admin_confirm_remove_leader",
                     "exec": _wrapper(caller, "leader_to_remove", leader)}
        options += (node_dict,)

    return text, options


def admin_confirm_remove_leader(caller):
    selected_org = caller.ndb._menutree.selected_org
    leader_to_remove = caller.ndb._menutree.leader_to_remove

    text = "Are you sure that you wish to remove %s from %s?  This action cannot be undone." % (
    leader_to_remove.db_member.name, selected_org.db_key)

    options = ({"desc": "Confirm",
                "exec": admin_do_remove_leader,
                "goto": "admin_edit_selected_org"},
               {"desc": "Cancel",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_do_remove_leader(caller):
    selected_org = caller.ndb._menutree.selected_org
    leader_to_remove = caller.ndb._menutree.leader_to_remove

    selected_org.db_leaders.filter(id=leader_to_remove.id).delete()


# ######################### EDIT MEMBERS ##########################################

def admin_edit_members(caller):
    selected_org = caller.ndb._menutree.selected_org
    text = "Org: %s" % selected_org.db_key

    members = selected_org.db_members.all()
    member_string = ""
    index = 0
    for member in members:
        if index < len(members) - 1:
            member_string += member.db_member.name + ", "
        else:
            member_string += member.db_member.name
        index += 1

    text += "\n\nMembers: %s" % member_string

    options = ({"desc": "Add Member",
                "goto": "admin_add_member"},
               {"desc": "Remove Member",
                "goto": "admin_remove_member"},
               {"desc": "Edit Member",
                "goto": "admin_edit_member"},
               {"desc": "Go Back",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_edit_member(caller):
    selected_org = caller.ndb._menutree.selected_org
    text = "Please select the member you wish to edit."

    members = selected_org.db_members.all()

    options = ()
    for member in members:
        node_dict = {"desc": member.db_member.name, "goto": "admin_show_edit_member",
                     "exec": _wrapper(caller, "selected_member", member)}
        options += (node_dict,)

    return text, options


def admin_show_edit_member(caller):
    selected_member = caller.ndb._menutree.selected_member
    assets = selected_member.db_assigned_assets.all()

    asset_string = ""
    index = 0
    for asset in assets:
        if index < len(assets) - 1:
            asset_string = asset.key + ", "
        else:
            asset_string = asset.key

    text = "|wName:|n %s\n|wRank:|n %s\n|wAssignment:|n %s\n|wAssigned Assets:|n %s" % (
    selected_member.db_member.name, selected_member.db_rank, selected_member.db_assignment, asset_string)

    options = ({"desc": "Edit Rank",
                "goto": "admin_edit_member_rank"},
               {"desc": "Edit Assignment",
                "goto": "admin_edit_member_assignment"},
               {"desc": "Edit Assigned Assets",
                "goto": "admin_edit_member_assets"},
               {"desc": "Go Back",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_edit_member_rank(caller):
    selected_member = caller.ndb._menutree.selected_member
    text = "|wCurrent Rank:|n %s\n\nPlease enter the rank you would like to set this member to." \
           % selected_member.db_rank

    options = ({"key": "_default",
                "exec": admin_set_member_rank,
                "goto": "admin_show_edit_member"},
               {"key": "cancel",
                "desc": "Cancel",
                "goto": "admin_show_edit_member"})

    return text, options


def admin_set_member_rank(caller, caller_input):
    new_rank = caller_input.strip()
    selected_member = caller.ndb._menutree.selected_member

    selected_member.db_rank = new_rank
    selected_member.save()


def admin_edit_member_assignment(caller):
    selected_member = caller.ndb._menutree.selected_member
    text = "|wCurrent Assignment:|n %s\n\nPlease enter the assignment you would like to set this member to." \
           % selected_member.db_assignment

    options = ({"key": "_default",
                "exec": admin_set_member_assignment,
                "goto": "admin_show_edit_member"},
               {"key": "cancel",
                "desc": "Cancel",
                "goto": "admin_show_edit_member"})

    return text, options


def admin_set_member_assignment(caller, caller_input):
    new_assignment = caller_input.strip()
    selected_member = caller.ndb._menutree.selected_member

    selected_member.db_assignment = new_assignment
    selected_member.save()


def admin_edit_member_assets(caller):
    ###################  NOT IMPLEMENTED YET ##########################
    pass


def admin_add_member(caller):
    text = "Type the name of the person you want to add as a member of this Organization"

    options = ({"key": "_default",
                "exec": admin_set_add_member,
                "goto": "admin_edit_selected_org"},
               {"desc": "Cancel",
                "key": "cancel",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_set_add_member(caller, caller_input):
    selected_org = caller.ndb._menutree.selected_org
    temp_name = caller_input.strip()
    member = search_object(temp_name)

    if member:
        new_member = OrgMember.objects.create(db_org=selected_org)
        new_member.db_member = member[0]
        new_member.save()

        selected_org.db_members.add(new_member)
        selected_org.save()
    else:
        caller.msg("|rError: Character not found.|n")


def admin_remove_member(caller):
    selected_org = caller.ndb._menutree.selected_org
    text = "Below are listed the members of %s.  Please select the member you wish to remove from the org." \
           % selected_org.db_key

    options = ()

    members = selected_org.db_members.all()

    for member in members:
        node_dict = {"desc": member.db_member.name, "goto": "admin_confirm_remove_member",
                     "exec": _wrapper(caller, "member_to_remove", member)}
        options += (node_dict,)

    return text, options


def admin_confirm_remove_member(caller):
    selected_org = caller.ndb._menutree.selected_org
    member_to_remove = caller.ndb._menutree.member_to_remove

    text = "Are you sure that you wish to remove %s from %s?  This action cannot be undone." % (
    member_to_remove.db_member.name, selected_org.db_key)

    options = ({"desc": "Confirm",
                "exec": admin_do_remove_member,
                "goto": "admin_edit_selected_org"},
               {"desc": "Cancel",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_do_remove_member(caller):
    selected_org = caller.ndb._menutree.selected_org
    member_to_remove = caller.ndb._menutree.member_to_remove

    selected_org.db_members.filter(id=member_to_remove.id).delete()


# ############################ EDIT CREDITS ######################################

def admin_edit_credits(caller):
    selected_org = caller.ndb._menutree.selected_org
    text = "|wCurrent Credits:|n %s\n\nPlease enter the amount you wish to set the org's credits to." \
           % selected_org.db_credits

    options = ({"key": "_default",
                "exec": admin_set_edit_credits,
                "goto": "admin_edit_selected_org"},
               {"key": "cancel",
                "desc": "Cancel",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_set_edit_credits(caller, caller_input):
    selected_org = caller.ndb._menutree.selected_org
    credits = int(caller_input.strip())
    selected_org.db_credits = credits
    selected_org.save()


def admin_edit_resources(caller):
    selected_org = caller.ndb._menutree.selected_org
    text = "|wCurrent Resources:|n %s\n\nPlease enter the amount you wish to set the org's resources to." \
           % selected_org.db_resources

    options = ({"key": "_default",
                "exec": admin_set_edit_resources,
                "goto": "admin_edit_selected_org"},
               {"key": "cancel",
                "desc": "Cancel",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_set_edit_resources(caller, caller_input):
    selected_org = caller.ndb._menutree.selected_org
    resources = int(caller_input.strip())
    selected_org.db_resources = resources
    selected_org.save()


def admin_edit_assets(caller):
    text = "This feature has not yet been implemented.  Please go back to continue."

    options = ({"desc": "Go Back",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_edit_status(caller):
    selected_org = caller.ndb._menutree.selected_org
    if selected_org.db_active:
        status_text = "Active"
        options = ({"desc": "Deactivate",
                    "exec": admin_swap_status,
                    "goto": "admin_edit_selected_org"},
                   {"desc": "Go Back",
                    "goto": "admin_edit_selected_org"})
    else:
        status_text = "Inactive"
        options = ({"desc": "Activate",
                    "exec": admin_swap_status,
                    "goto": "admin_edit_selected_org"},
                   {"desc": "Go Back",
                    "goto": "admin_edit_selected_org"})

    text = "%s is currently %s.  Choose your action below." % (titlecase(selected_org.db_key), status_text)

    return text, options


def admin_swap_status(caller):
    selected_org = caller.ndb._menutree.selected_org
    selected_org.db_active = not selected_org.db_active
    selected_org.save()


def admin_edit_motd(caller):
    selected_org = caller.ndb._menutree.selected_org
    text = "|wCurrent Message of the Day:|n %s\n\nPlease enter the new MotD you wish to display.\n\n|yNote:|n Do not " \
           "start the description with the word 'cancel'." % selected_org.db_motd
    options = ({"key": "_default",
                "exec": admin_set_edit_motd,
                "goto": "admin_edit_selected_org"},
               {"key": "cancel",
                "desc": "Cancel",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_set_edit_motd(caller, caller_input):
    selected_org = caller.ndb._menutree.selected_org
    motd = caller_input.strip()
    selected_org.db_motd = motd
    selected_org.save()


def admin_edit_hq(caller):
    selected_org = caller.ndb._menutree.selected_org
    text = "Please select the planet where the Org is headquartered"
    planets = Tag.objects.filter(db_category="planet")

    options = _get_planets(caller)

    return text, options


def admin_edit_hq_zone(caller):
    temp_planet = caller.ndb._menutree.hq_planet
    text = "Please select the zone on %s where the Organization is headquartered" % titlecase(temp_planet)
    options = _get_zones(caller, temp_planet)
    return text, options


def admin_confirm_edit_hq(caller):
    selected_org = caller.ndb._menutree.selected_org
    new_hq = caller.ndb._menutree.temp_org_hq
    text = "Are you sure you with to change the Headquarters of %s from %s to %s?" % (
    selected_org.db_key, selected_org.db_headquarters, new_hq[0].key)

    options = ({"desc": "Confirm",
                "exec": admin_set_new_hq,
                "goto": "admin_edit_selected_org"},
               {"desc": "Cancel",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_set_new_hq(caller):
    selected_org = caller.ndb._menutree.selected_org
    new_hq = caller.ndb._menutree.temp_org_hq[0]

    selected_org.db_headquarters = new_hq
    selected_org.save()


def admin_edit_branches(caller):
    selected_org = caller.ndb._menutree.selected_org
    pass


def admin_edit_desc(caller):
    selected_org = caller.ndb._menutree.selected_org
    text = "|wCurrent Description:|n %s\n\nPlease enter the new description you wish to display.\n\n|yNote:|n Do not " \
           "start the description with the word 'cancel'." % selected_org.db_desc
    options = ({"key": "_default",
                "exec": admin_set_edit_description,
                "goto": "admin_edit_selected_org"},
               {"key": "cancel",
                "desc": "Cancel",
                "goto": "admin_edit_selected_org"})

    return text, options


def admin_set_edit_description(caller, caller_input):
    selected_org = caller.ndb._menutree.selected_org
    new_desc = caller_input.strip()

    selected_org.db_desc = new_desc
    selected_org.save()


def admin_view_orgs(caller):
    table = evtable.EvTable("Name", "Leader", "Mbrs", "HQ", border="header", header_line_char='-')
    orgs = Org.objects.all()

    for org in orgs:
        mem_count = org.db_members.count()
        leader = org.db_leaders.first().db_member
        temp_hq = org.db_headquarters
        zone = None
        if bool(temp_hq) is True:
            zone = titlecase(temp_hq.tags.get(category="zonemaster"))

        table.add_row(org.db_key, leader, mem_count, zone)

    table.reformat_column(0, width=25)
    table.reformat_column(1, width=25)
    table.reformat_column(2, width=6, align="r")
    table.reformat_column(3, width=24)

    text = table

    options = ({"desc": "Go Back",
                "goto": "menu_start_node"})

    return text, options


def admin_setup_org(caller):
    text = "Please enter the name of the Org you would like to create.  Note: This name must be unique.  If you are " \
           "unsure, cancel and check the Org list for the names of existing Orgs."

    options = ({"key": "_default",
                "exec": set_admin_create_org,
                "goto": "admin_set_org_desc"},
               {"desc": "Cancel",
                "key": "cancel",
                "goto": "menu_start_node"})
    return text, options


def set_admin_create_org(caller, caller_input):
    org_name = caller_input.strip()
    setattr(caller.ndb._menutree, 'temp_orgname', org_name)


def admin_set_org_desc(caller):
    org_name = caller.ndb._menutree.temp_orgname
    text = "Org Name: %s\n\nPlease enter a description of the Organization. (maximum of 250 character)" % org_name

    options = ({"key": "_default",
                "exec": set_admin_org_desc,
                "goto": "admin_set_org_leaders"},
               {"desc": "Cancel",
                "key": "cancel",
                "goto": "menu_start_node"})

    return text, options


def set_admin_org_desc(caller, caller_input):
    org_desc = caller_input.strip()
    setattr(caller.ndb._menutree, "temp_org_desc", org_desc)


def admin_set_org_leaders(caller):
    org_name = caller.ndb._menutree.temp_orgname
    org_desc = caller.ndb._menutree.temp_org_desc

    text = "Org Name: %s\nOrg Description: %s\n\nPlease type the name of a Character that will act as a leader of " \
           "this org.  (Others leaders can be added later)" % (org_name, org_desc)

    options = ({"key": "_default",
                "exec": set_admin_org_leader,
                "goto": "admin_set_org_options"},
               {"key": "cancel",
                "desc": "Cancel",
                "goto": "menu_start_node"})

    return text, options


def set_admin_org_leader(caller, caller_input):
    temp_name = caller_input.strip()
    leader = search_object(temp_name)
    setattr(caller.ndb._menutree, "temp_org_leader", leader)


def admin_set_org_options(caller):
    if not caller.ndb._menutree.temp_org_leader:
        text = "Character not found.  Please enter a valid character to be elected to leader of the org."

        options = ({"key": "_default",
                    "exec": set_admin_org_leader,
                    "goto": "admin_set_org_options"},
                   {"key": "cancel",
                    "desc": "Cancel",
                    "goto": "menu_start_node"})

        return text, options

    else:
        org_name = caller.ndb._menutree.temp_orgname
        org_desc = caller.ndb._menutree.temp_org_desc
        org_leader = caller.ndb._menutree.temp_org_leader
        text = "Org Name: %s\nOrg Description: %s\nOrg Leader: %s" % (org_name, org_desc, org_leader[0].name)

        options = ()

        if hasattr(caller.ndb._menutree, "temp_org_credits"):
            text += "\nStarting Credits: %s" % caller.ndb._menutree.temp_org_credits
            options += ({"desc": "|xStarting Credits|n",
                         "goto": "admin_set_starting_credits"},)
        else:
            options += ({"desc": "Starting Credits",
                         "goto": "admin_set_starting_credits"},)

        if hasattr(caller.ndb._menutree, "temp_org_resources"):
            text += "\nStarting Resources: %s" % caller.ndb._menutree.temp_org_resources
            options += ({"desc": "|xStarting Resources|n",
                         "goto": "admin_set_starting_resources"},)
        else:
            options += ({"desc": "Starting Resources",
                         "goto": "admin_set_starting_resources"},)

        if hasattr(caller.ndb._menutree, "temp_org_hq"):
            text += "\nHeadquarters: %s" % caller.ndb._menutree.temp_org_hq[0].key
            options += ({"desc": "|xSet Headquarters|n",
                         "goto": "admin_set_headquarters"},)
        else:
            options += ({"desc": "Set Headquarters",
                         "goto": "admin_set_headquarters"},)

        text += "\n\nPlease select the org options you wish to set or select Finish to create the Organization.  If " \
                "the option is darkened, it means that the option has already been set.  However you can change it " \
                "at any time prior to selecting Finish."

        options += ({"desc": "Finish",
                     "key": "finish",
                     "goto": "admin_finish_org_create"},)
        return text, options


def admin_set_starting_credits(caller):
    text = "Please enter the amount of starting credits for the org."

    options = ({"key": "_default",
                "exec": set_admin_starting_credits,
                "goto": "admin_set_org_options"})

    return text, options


def set_admin_starting_credits(caller, caller_input):
    try:
        temp_credits = int(caller_input.strip())
        setattr(caller.ndb._menutree, "temp_org_credits", temp_credits)
    except ValueError:
        caller.msg("|rError: Value entered is not a number.  Credits not set.|n")


def admin_set_starting_resources(caller):
    text = "Please enter the amount of starting resources you wish to set."

    options = ({"key": "_default",
                "exec": set_admin_starting_resources,
                "goto": "admin_set_org_options"})

    return text, options


def set_admin_starting_resources(caller, caller_input):
    try:
        temp_resources = int(caller_input.strip())
        setattr(caller.ndb._menutree, "temp_org_resources", temp_resources)
    except ValueError:
        caller.msg("|rError: Value entered is not a number.  Credits not set.|n")


def admin_set_headquarters(caller):
    text = "Please select the planet where the Org is headquartered"
    planets = Tag.objects.filter(db_category="planet")

    options = _get_planets(caller)
    return text, options


def admin_set_hq_zone(caller):
    temp_planet = caller.ndb._menutree.hq_planet

    text = "Please select the zone on %s where the Organization is headquartered" % titlecase(temp_planet)

    options = _get_zones(caller, temp_planet)

    return text, options


def admin_finish_org_create(caller):
    org_name = caller.ndb._menutree.temp_orgname
    org_desc = caller.ndb._menutree.temp_org_desc
    org_leader = caller.ndb._menutree.temp_org_leader

    text = "Org Name: %s\nOrg Description: %s\nOrg Leader: %s" % (org_name, org_desc, org_leader[0].name)

    if hasattr(caller.ndb._menutree, "temp_org_credits"):
        text += "\nStarting Credits: %s" % caller.ndb._menutree.temp_org_credits
    if hasattr(caller.ndb._menutree, "temp_org_resources"):
        text += "\nStarting Resources: %s" % caller.ndb._menutree.temp_org_resources
    if hasattr(caller.ndb._menutree, "temp_org_hq"):
        text += "\nHeadquarters: %s" % caller.ndb._menutree.temp_org_hq[0].key

    text += "\n\nPlease review the above information.  If it looks right, then confirm by typing |wFinish|n again.  " \
            "Otherwise you may |wGo Back|n to correct an errors."

    options = ({"desc": "Finish",
                "goto": "menu_start_node",
                "exec": admin_create_org},
               {"desc": "Go Back",
                "goto": "admin_set_org_options"})

    return text, options


def admin_create_org(caller):
    org_name = caller.ndb._menutree.temp_orgname
    org_desc = caller.ndb._menutree.temp_org_desc
    org_leader = caller.ndb._menutree.temp_org_leader
    org_credits = int(getattr(caller.ndb._menutree, 'temp_org_credits', 0))
    org_resources = int(getattr(caller.ndb._menutree, "temp_org_resources", 0))
    org_hq = getattr(caller.ndb._menutree, "temp_org_hq", None)

    new_org = Org.objects.create(db_key=org_name, db_desc=org_desc, db_credits=org_credits, db_resources=org_resources,
                                 db_active=True)
    new_member = OrgMember.objects.create(db_org=new_org)
    new_member.db_member = org_leader[0]
    new_member.save()

    new_org.db_leaders.add(new_member)
    if org_hq:
        new_org.db_headquarters = org_hq[0]
    new_org.save()


#  UTILITY FUNCTIONS

def _wrapper(caller, attr, value):
    return lambda caller: setattr(caller.ndb._menutree, attr, value)


def _get_planets(caller):
    planets = Tag.objects.filter(db_category="planet")

    options = ()

    for planet in planets:
        node_dict = {"desc": titlecase(planet.db_key), "goto": "admin_edit_hq_zone",
                     "exec": _wrapper(caller, "hq_planet", planet.db_key)}
        options += (node_dict,)

    return options


def _get_zones(caller, planet):
    planet_rooms = evennia.search_tag(planet)
    zones = []
    for planet in planet_rooms:
        zone = planet.tags.get(category="zonemaster")
        zones.append(zone)

    options = ()

    for zone in zones:
        node_dict = {"desc": titlecase(zone), "goto": "admin_confirm_edit_hq",
                     "exec": _wrapper(caller, "temp_org_hq", evennia.search_tag(zone, "zonemaster"))}
        options += (node_dict,)

    return options
