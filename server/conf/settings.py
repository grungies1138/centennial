"""
Evennia settings file.

The available options are found in the default settings file found
here:

/home/ubuntu/mush/evennia/evennia/settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Star Wars: Centennial"

INSTALLED_APPS = INSTALLED_APPS + ("bbs", "jobs", "orgs", "web.character",)

INLINEFUNC_ENABLED = True
MULTISESSION_MODE = 1

DEBUG = True

PROTOTYPE_MODULES = ["world.prototypes", "world.weapon_prototypes", "world.armor_prototypes", "world.equipment_prototypes",
                     "world.consumable_prototypes"]

GUEST_ENABLED = True
GUEST_LIST = ['Guest1', 'Guest2', 'Guest3', 'Guest4', 'Guest5', 'Guest6', 'Guest7', 'Guest8', 'Guest9']

# Server ports. If enabled and marked as "visible", the port
# should be visible to the outside world on a production server.
# Note that there are many more options available beyond these.

# Telnet ports. Visible.
TELNET_ENABLED = True
TELNET_PORTS = [4000]
# (proxy, internal). Only proxy should be visible.
WEBSERVER_ENABLED = True
WEBSERVER_PORTS = [(4001, 4002)]
# Telnet+SSL ports, for supporting clients. Visible.
SSL_ENABLED = False
SSL_PORTS = [4003]
# SSH client ports. Requires crypto lib. Visible.
SSH_ENABLED = False
SSH_PORTS = [4004]
# Websocket-client port. Visible.
WEBSOCKET_CLIENT_ENABLED = True
WEBSOCKET_CLIENT_PORT = 4005
# Internal Server-Portal port. Not visible.
AMP_PORT = 4006

# TIME SETTINGS
TIME_GAME_EPOCH = 0

TIME_FACTOR = 3

TIME_UNITS = {"sec": 1,
              "min": 60,
              "hour": 60 * 60,
              "day": 60 * 60 * 24,
              "week": 60 * 60 * 24 * 5,
              "month": 60 * 60 * 24 * 5 * 7,
              "year": 60 * 60 * 24 * 5 * 7 * 10 + 60 * 60 * 24 * 5 * 3 + 60 * 60 * 24 * 3}

OLD_REPUBLIC = 799935436800

TREAT_OF_CORUSCANT = 119454566400

RUUSAN_REFORMATION = 35101900800

GREAT_RESYNCHRONIZATION = 4419532800

BATTLE_OF_YAVIN = 3306700800

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
