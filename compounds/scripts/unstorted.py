#!/usr/bin/python
# _*_ coding:utf-8 _*_
import csv

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatcm.settings')
import django
django.setup()

from compounds.models import Compound

compounds = Compound.objects.filter(mol=None)

with open("unstorted_compound.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    for c in compounds:
        writer.writerow(
            [c.chinese_name.encode("ascii", 'ignore'),
             c.english_name.encode("ascii", 'ignore'),
             c.smiles.encode("ascii", 'ignore')]
        )