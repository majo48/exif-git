""" main part of the recreate-git application
    Copyright (c) 2021 M. Jonasse (martin.jonasse@mail.ch)
"""
from recreate import app

if __name__ == "__main__":
    # execute only if run as a script
    app.manage_arguments()