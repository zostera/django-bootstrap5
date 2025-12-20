#!/usr/bin/env python
import os
import sys

try:
    import django

    django_version = django.get_version()
except Exception:
    django_version = "not available"

if "test" in sys.argv:
    print(f"* Python {sys.version.split()[0]}\n* Django {django_version}")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.app.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
