import os
import xlrd
import logging
from functools import partial
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'yatcm.settings')
import django
django.setup()
from compounds.models import *  #NOQA
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import multiprocessing
from threading import Thread


CORES = multiprocessing.cpu_count()

logging.basicConfig(
    level=logging.WARNING,
    format="[%(message)s]",
    filename="/home/jianping/workspace/hz_work_home/logs/identity_log.txt",
    filemode='w'
)


structure_file = "/home/jianping/workspace/hz_work_home/data/data_base_result/34680_last_compound.xlsx"


def extract_names(cell):
    return cell.split("\n")


def upload_identity(row):
    cn_names = extract_names(row[0])
    en_names = extract_names(row[1])
    synonyms = extract_names(row[2])

    for cn_name in cn_names:
        if cn_name:
            ChineseIdentity.objects.get_or_create(identity=cn_name)

    for en_name in en_names:
        if en_name:
            EnglishIdentity.objects.get_or_create(identity=en_name)

    for synonym in synonyms:
        if synonym:
            EnglishIdentity.objects.get_or_create(identity=synonym)


def upload(file_name):
    table = xlrd.open_workbook(file_name).sheet_by_index(0)
    nrows = table.nrows
    for row_number in range(1, nrows):
        row = table.row_values(row_number)
        upload_identity(row)

if __name__ == '__main__':
    upload(structure_file)