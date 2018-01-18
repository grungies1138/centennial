"""
Server startstop hooks

This module contains functions called by Evennia at various
points during its startup, reload and shutdown sequence. It
allows for customizing the server operation as desired.

This module must contain at least these global functions:

at_server_start()
at_server_stop()
at_server_reload_start()
at_server_reload_stop()
at_server_cold_start()
at_server_cold_stop()

"""
from evennia import create_script
from evennia.scripts.models import ScriptDB
import subprocess
from world import languages


def at_server_start():
    """
    This is called every time the server starts up, regardless of
    how it was shut down.
    """
    if len(ScriptDB.objects.filter(db_key="weather")) == 0:
        create_script("world.weather.WeatherScript", key="weather", persistent=True, obj=None)
    #languages.setup_languages()


def at_server_stop():
    """
    This is called just before the server is shut down, regardless
    of it is for a reload, reset or shutdown.
    """
    pass


def at_server_reload_start():
    """
    This is called only when server starts back up after a reload.
    """
    pass


def at_server_reload_stop():
    """
    This is called only time the server stops before a reload.
    """
    print("Starting git pull")
    process = subprocess.Popen("git pull origin master", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if out:
        print(out)
    if err:
        print(err)

    print("git pull completed.")


def at_server_cold_start():
    """
    This is called only when the server starts "cold", i.e. after a
    shutdown or a reset.
    """
    pass


def at_server_cold_stop():
    """
    This is called only when the server goes down due to a shutdown or
    reset.
    """
    pass
