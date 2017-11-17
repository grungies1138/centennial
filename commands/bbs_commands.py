import datetime
import time
from typeclasses.characters import Character
from evennia import Command as BaseCommand
from evennia import default_cmds
from evennia.utils import create, utils, evtable
from bbs.models import Board, Post, Comment
from commands.library import titlecase, notify, HEAD_CHAR, SUB_HEAD_CHAR
from evennia.utils import evmore
from evennia.utils.evmenu import EvMenu
from commands.library import node_formatter, options_formatter

HELP_CATEGORY = "BBS"


class CreateBoardCommand(default_cmds.MuxCommand):
    """
    Create a new Bulletin Board.
    Usage:
        +bbcreate <name>=<description>
    """

    key = "+bbcreate"
    aliases = ["bbcreate"]
    lock = "cmd:perm(Wizard)"
    help_category = HELP_CATEGORY

    def func(self):
        if not self.args:
            self.caller.msg("You must supply a valid name and description.")
            return
        else:
            new_board = Board(db_key=self.lhs, db_timeout=-1, db_description=self.rhs)

            new_board.locks.add("read:all()")
            new_board.save()
            self.caller.msg("Board successfully created.")


class LockBoardCommand(default_cmds.MuxCommand):
    """
    Adds a lock to a board.
    Usage:
        +bblock <#>=<lockstring>
    """

    key = "+bblock"
    aliases = ["bblock"]
    lock = "cmd:perm(Wizard)"
    help_category = HELP_CATEGORY

    def func(self):
        board = Board.objects.filter(id=self.lhs).first()
        board.locks.add("%s" % self.rhs)
        board.save()
        self.caller.msg("Lock added successfully")


class ViewAllBoardsCommand(default_cmds.MuxCommand):
    """
    Shows a list of all boards that you could join.
    """

    key = "+bblist"
    aliases = {"bblist"}
    lock = "cmd:all()"
    help_category = HELP_CATEGORY

    def func(self):
        boards = Board.objects.all()
        viewable_boards = []

        for board in boards:
            if board.locks.check(self.caller, access_type='read'):
                viewable_boards.append(board)

        table = evtable.EvTable("{wID:{n", "{wTitle:{n", "{wLast Post:{n", "{wTotal Posts:{n", table=None,
                                border='header', header_line_char="-", width=78)
        index = 1
        for board in viewable_boards:
            if board.db_posts.all().order_by('db_date_posted').first():
                table.add_row(index, board.db_key,
                              board.db_posts.all().order_by('db_date_posted').first().db_date_posted,
                              board.db_posts.count())
            else:
                table.add_row(index, board.db_key, "None",
                              board.db_posts.count())
            index += 1

        table.reformat_column(0, width=6)
        table.reformat_column(1, width=38)
        table.reformat_column(2, width=20)
        table.reformat_column(3, width=14)
        self.caller.msg(HEAD_CHAR * 78)
        self.caller.msg(" BBLIST ".center(78))
        self.caller.msg(SUB_HEAD_CHAR * 78)
        self.caller.msg(table)
        self.caller.msg(HEAD_CHAR * 78)
        return


class JoinBoardCommand(default_cmds.MuxCommand):
    """
    Command to join a listed Board
    Usage:
        +bbjoin <#>
    """

    key = "+bbjoin"
    aliases = ["bbjoin"]
    lock = "cmd:all()"
    help_category = HELP_CATEGORY

    def func(self):
        if not self.args:
            self.caller.msg("You must supply a board ID to join.")
            return
        else:
            board_to_join = Board.objects.all()[int(self.args) - 1]
            board_to_join.db_members.add(self.caller)
            board_to_join.save()
            self.caller.msg("Successfully Joined Board %s" % self.args)
            return


class LeaveBoardCommand(default_cmds.MuxCommand):
    """
    Command used to unjoin or leave a board.
    Usage:
        +bbleave <#>
    """

    key = "+bbleave"
    aliases = ["bbleave"]
    lock = "cmd:all()"
    help_category = HELP_CATEGORY

    def func(self):
        if not self.args:
            self.caller.msg("You must supply a board ID to leave.")
            return
        else:
            board_to_leave = Board.objects.get(id=self.args)
            if board_to_leave:
                board_to_leave.db_members.remove(self.caller)
                self.caller.msg("Successfully left Board %s" % self.args)
                return
            else:
                self.caller.msg("Board not Found.")
                return


class ViewBoardsCommand(default_cmds.MuxCommand):
    """
    View all available boards
    Usage:
        +boards
    """

    key = "+boards"
    aliases = ["boards"]
    lock = "cmd:all()"
    help_category = HELP_CATEGORY

    def func(self):
        if not self.switches:
            member_boards = []
            boards = Board.objects.all()
            for board in boards:
                if board.db_members.filter(id=self.caller.id).first():
                    member_boards.append(board)

            if member_boards:
                table = evtable.EvTable("{wID:{n", "{wTitle:{n", "{wLast Post:{n", "{wTotal Posts:{n", table=None,
                                        border='header', header_line_char=SUB_HEAD_CHAR, width=78)

                index = 1
                for board in member_boards:
                    if board.db_posts.all().order_by('db_date_posted').first():
                        table.add_row(index, board.db_key,
                                      board.db_posts.all().order_by('db_date_posted').first().db_date_posted,
                                      board.db_posts.count())
                    else:
                        table.add_row(index, board.db_key, "None",
                                      board.db_posts.count())
                    index += 1

                table.reformat_column(0, width=6)
                table.reformat_column(1, width=38)
                table.reformat_column(2, width=20)
                table.reformat_column(3, width=14)
                self.caller.msg(HEAD_CHAR * 78)
                self.caller.msg(table)
                self.caller.msg(HEAD_CHAR * 78)
            else:
                self.caller.msg("You do not belong to any boards.")
                return


class DeleteBoardCommand(default_cmds.MuxCommand):
    """
    Wizard only command to remove a board.
    Usage:
        +bbdelete <#>
    """

    key = "+bbdelete"
    aliases = ["bbdelete"]
    lock = "perm(Wizard)"
    help_category = HELP_CATEGORY

    def func(self):
        if not self.args:
            self.caller.msg("You must supply a Board ID to delete.")
            return
        else:
            board_to_delete = Board.objects.get(id=self.args)
            if not board_to_delete:
                self.caller.msg("Board %s does not exist." % self.args)
                return
            else:
                Board.objects.filter(id=board_to_delete.id).delete()
                self.caller.msg("Board %s successfully deleted" % self.args)
                return


class DeletePostCommand(default_cmds.MuxCommand):
    """
    Allows board posts to be deleted by the poster or by admin
    Usage +bbremove <#>/<#>
    """

    key = "+bbremove"
    aliases = ["bbremove"]
    lock = "cmd:all()"
    help_category = HELP_CATEGORY

    def func(self):
        if not self.args or not "/" in self.args:
            self.caller.msg("You must supply a Board & Post ID to delete a post")
            return
        board, post = self.args.split("/", 1)
        board_to_read = Board.objects.filter(id=board).first()
        if not board_to_read:
            self.caller.msg("That board does not exist")
            return
        post_to_delete = board_to_read.db_posts.all()[int(post) - 1]

        if self.caller.key in post_to_delete.db_sender or \
                self.caller.locks.check_lockstring(self.caller, "dummy:perm(Wizards)"):
            Post.objects.filter(id=post_to_delete.id).delete()
            self.caller.msg("Post successfully deleted.")
        else:
            self.caller.msg("You do not have permission to remove that post.")


class ReadBoardCommand(default_cmds.MuxCommand):
    """
    Set of commands for reading boards and posts.
    Usage:
        +bbread
            - Shows the boards you are a member of and the current unread posts in each.
        +bbread <#>
            - Shows all posts in a particular board.
        +bbread <#>/<#>
            - Displays the requested post from the indicated board
    """

    key = "+bbread"
    aliases = ["bbread"]
    lock = "cmd:all()"
    help_category = HELP_CATEGORY

    def func(self):
        if not self.args:
            member_boards = []

            boards = Board.objects.all()
            for board in boards:
                if board.db_members.filter(id=self.caller.id).first():
                    member_boards.append(board)

                board_posts = board.db_posts.all()

            if member_boards:
                table = evtable.EvTable("{wID:{n", "{wTitle:{n", "{wLast Post:{n", "{wUnread:{n", table=None,
                                        border='header', header_line_char=SUB_HEAD_CHAR, width=78)
                index = 1
                for board in member_boards:
                    unread_posts = 0
                    for post in board.db_posts.all():
                        if self.caller not in post.db_has_read.all():
                            unread_posts += 1
                    if board.db_posts.all().order_by('db_date_posted').first():
                        table.add_row(index, board.db_key,
                                      board.db_posts.all().order_by('db_date_posted').first().db_date_posted,
                                      unread_posts)
                    else:
                        table.add_row(index, board.db_key, "None",
                                      unread_posts)
                    index += 1

                table.reformat_column(0, width=6)
                table.reformat_column(1, width=38)
                table.reformat_column(2, width=20)
                table.reformat_column(3, width=14)
                self.caller.msg(HEAD_CHAR * 78)
                self.caller.msg(table)
                self.caller.msg(HEAD_CHAR * 78)
            else:
                self.caller.msg("You do not belong to any boards.")
                return
        elif "/" in self.lhs:
            board, post = self.lhs.split("/", 1)

            board_to_read = Board.objects.filter(id=board).first()
            if not board_to_read:
                self.caller.msg("That board does not exist.")
                return

            board_posts = board_to_read.db_posts.all()
            if int(post) > len(board_posts):
                self.caller.msg("That is not a valid post.  Please review the post list and try again.")
                return
            post_to_read = board_posts[int(post) - 1]
            if not post_to_read:
                self.caller.msg("There was an error retrieving the post.  Please contact an Admin.")
                return
            if post_to_read not in board_posts:
                self.caller.msg("That post is not a member of that board.")
                return
            post_to_read.db_has_read.add(self.caller)
            self.caller.msg("Likes: {}".format(post_to_read.db_likes))

            post_form = []
            post_form.append(HEAD_CHAR * 78)
            post_form.append(board_to_read.db_key.center(78))
            post_form.append(SUB_HEAD_CHAR * 78)
            post_form.append("{wSubject:{n %s  {wPosted By:{n %s  {wDate Posted:{n %s" %
                             (post_to_read.db_key, post_to_read.db_sender,
                              post_to_read.db_date_posted.strftime("%m/%d/%Y %H:%M:%S")))
            post_form.append(SUB_HEAD_CHAR * 78)
            post_form.append(post_to_read.db_message)
            post_form.append("-" * 78)
            post_form.append(
                "{wComments:{n %s  {wLikes:{n %s" % (post_to_read.db_comments.count(), str(post_to_read.db_likes)))
            post_form.append(HEAD_CHAR * 78)
            post_form.append("")

            comment_count = 0
            for comment in post_to_read.db_comments.all():
                comment_count += 1
                post_form.append("{wComment %s{n" % comment_count)
                post_form.append("")
                post_form.append("{wAuthor:{n %s  {wDate Posted:{n %s  {wLikes:{n %s" %
                                 (comment.db_author, comment.db_date_posted, comment.db_likes))
                post_form.append("")
                post_form.append(comment.db_message)
                post_form.append(SUB_HEAD_CHAR * 78)

            evmore.msg(self.caller, "\n".join(post_form))
            # self.caller.msg("\n".join(post_form))


        else:
            board = self.lhs
            board_to_display = Board.objects.all()[int(board) - 1]
            if not board_to_display:
                self.caller.msg("That board does not exist.")
                return
            board_posts = board_to_display.db_posts.all()
            table = evtable.EvTable("", "{wID:{n", "{wSubject:{n", "{wDate Posted:{n", "{wComments:{n", "{wLikes:{n",
                                    table=None, border='header', header_line_char=SUB_HEAD_CHAR, width=78)
            index = 1
            for post in board_posts:
                read = ""
                if self.caller not in post.db_has_read.all():
                    read = "U"
                else:
                    read = " "

                table.add_row(read, index, post.db_key, post.db_date_posted.strftime("%m/%d/%Y"),
                              post.db_comments.count(), post.db_likes)
                index += 1

            table.reformat_column(0, width=3)
            table.reformat_column(1, width=5)
            table.reformat_column(2, width=30)
            table.reformat_column(3, width=20)
            table.reformat_column(4, width=11)
            table.reformat_column(5, width=8)

            self.caller.msg(HEAD_CHAR * 78)
            self.caller.msg(table)
            self.caller.msg(HEAD_CHAR * 78)


class AddPostCommand(default_cmds.MuxCommand):
    """
    Add a new Post to a board
    Usage:
        +bbpost <board Number>=<title>/<message>
    """

    key = "+bbpost"
    aliases = ["bbpost"]
    lock = "cmd:all()"
    help_category = HELP_CATEGORY

    def func(self):
        if not self.args:
            self.caller.msg("You must supply arguments.  Try again, moron.")
            return
        elif not self.rhs:
            self.caller.msg("You much provide a title and a message to make a post.")
            return
        else:
            title, message = self.rhs.split("/")
            new_post = Post(db_key=title, db_message=message, db_sender=self.caller, db_likes=0,
                            db_date_posted=datetime.datetime.now())
            new_post.save()

            board_posted_to = Board.objects.all()[int(self.lhs) - 1]

            board_posted_to.db_posts.add(new_post)
            board_posted_to.save()
            # self.caller.msg("Post '%s' successfully posted to %s Board" % (titlecase(title), board_posted_to.db_key))
            notify_lockstring = ""
            for member in board_posted_to.db_members.all():
                notify(self.caller, "dummy:id(%s)" % member.id,
                       "New post added to the %s board." % board_posted_to.db_key)


class AddPostCommentCommand(default_cmds.MuxCommand):
    """
    add a comment to an existing post.
    Usage:
        +bbcomment <board>/<post>=<comment>
    """

    key = "+bbcomment"
    aliases = ["bbcomment"]
    lock = "cmd:all()"
    help_category = HELP_CATEGORY

    def func(self):
        if not self.args:
            self.caller.msg("You must supply arguents.  Try again, moron.")
            return
        elif "/" in self.lhs:
            board, post = self.lhs.split("/", 1)
            post_to_read = None
            board_to_read = Board.objects.filter(id=board).first()
            if not board_to_read:
                self.caller.msg("That is not a valid board.  Please try again.")
                return
            conn = board_to_read.db_posts.through.objects.filter(post__id=post)[0];
            if conn:
                post_to_read = conn.post

            if not post_to_read:
                self.caller.msg("That is not a valis post.  Please try again.")
                return

            new_comment = Comment(db_author=self.caller.key, db_message=self.rhs.strip(), db_likes=0,
                                  db_date_posted=datetime.datetime.now())
            new_comment.save()

            post_to_read.db_comments.add(new_comment)
            post_to_read.save()

            # self.caller.msg("Comment added to Post %s on %s" % (post, board_to_read.db_key))
            for member in board_to_read.db_members.all():
                notify(self.caller, "dummy:id(%s)" % member.id,
                       "New Comment added to Post %s on the %s board" % (post, board_to_read.db_key))


class LikeCommand(default_cmds.MuxCommand):
    """
    Adds a like to a board Post or Comment.
    Usage:
        +bblike <board>/<post>[/<comment>]
        Board and post are required.  Comment is optional, but required to like a comment.
        Ex: +bblike 1/4/2 (likes the second comment on the fourth post on the first board.)
    """

    key = "+bblike"
    aliases = ["bblike"]
    lock = "cmd:all()"
    help_category = HELP_CATEGORY

    def func(self):
        if not self.args:
            self.caller.msg("You must supply arguments.  Try again, moron.")
            return

        board = None
        post = None
        comment = None

        if not "/" in self.lhs:
            self.caller.msg("Invalid argument.  Check the help file and try again.")
            return
        else:
            if len(self.args.split("/", self.args.count("/") + 1)) > 2:
                board, post, comment = self.args.split("/")
            else:
                board, post = self.args.split("/")

            board_to_read = Board.objects.filter(id=board).first()
            post_to_read = None
            comment_to_read = None
            post_to_read = board_to_read.db_posts.all()[int(post) - 1]

            if comment:
                comment_conn = [c for c in post_to_read.db_comments.filter(id=comment)][0]
                if comment_conn:
                    comment_to_read = comment_conn.comment

            if comment_to_read:
                if not self.caller in comment_to_read.db_has_liked.all():
                    comment_to_read.db_likes += 1

                    comment_to_read.db_has_liked.add(self.caller)
                    comment_to_read.save()
                    self.caller.msg("Successfully liked Comment %s on Post %s on %s" %
                                    (comment_to_read.id, post_to_read.id, board_to_read.db_key))
            elif post_to_read:
                if not self.caller in post_to_read.db_has_liked.all():
                    post_to_read.db_likes += 1

                    post_to_read.db_has_liked.add(self.caller)
                    post_to_read.save()
                    self.caller.msg("Successfully liked Post %s on %s" % (post_to_read.id, board_to_read.db_key))
                else:
                    self.caller.msg("You have already liked this item.")
            else:
                self.caller.msg("Invalid Post or Comment.  Please verify the numbers and try again.")


class BBSCommand(default_cmds.MuxCommand):
    """
    Command to interact with the BBS system.
    """

    key = "+bbs"
    aliases = []
    locks = "cmd:all()"
    help_category = HELP_CATEGORY

    def func(self):
        EvMenu(self.caller, "commands.bbs_commands",
               startnode="menu_start_node",
               cmdset_mergetype="Replace",
               node_formatter=node_formatter,
               auto_help=False,
               options_formatter=options_formatter,
               cmd_on_exit=exit_message)


def menu_start_node(caller):
    text = "Welcome to GhostBBS.  Here you will be able to view, post and reply to posts made on a variety of bulliten boards.  Feel free to look over the options listed below and enjoy."

    options = ({"desc": "Boards",
                "goto": "list_boards"},)

    if caller.locks.check_lockstring(caller, "dummy:perm(Wizards)"):
        options += ({"desc": "Administration",
                     "goto": "board_admin"},)

    return text, options


def exit_message(caller, menu):
    caller.msg("Exiting +orgs.  Goodbye.")