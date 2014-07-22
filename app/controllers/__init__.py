# -*- coding: utf-8 -*-
"""
    ICE
    ~~~~~~

    A customer management application provided 
    to the Ice Sports Forum.

    :copyright: (c) 2014 by Zackery Field.
    :license: BSD, see LICENSE for more details.
"""

from parse_csv import CSV_to_dict as dictize
from ..database import db
from ..models import Customer, Laser, Visit, Users, Schedule
