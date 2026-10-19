"""Paid advertisers on Specialty pages, keyed by service slug (or family slug for a whole group).

Each entry: dict(name, area, phone, url, featured=False). Empty until advertisers sign up;
pages then show an "Advertise here" slot instead.
"""

ADS = {}
