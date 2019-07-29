import os

def run_command_in_new_gnome_session(command: str):
    os.system(f"gnome-terminal -x {command}")