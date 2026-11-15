#!/usr/bin/env python
"""Run Django management commands from the repository root."""
import os
import sys

from django.core.management import execute_from_command_line


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")
    execute_from_command_line(sys.argv)
