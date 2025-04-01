""" main part of the rename-git application
    Copyright (c) 2021 Martin Jonasse
"""
from rename import app

if __name__ == "__main__":
    # execute only if run as a script
    app.manage_arguments()