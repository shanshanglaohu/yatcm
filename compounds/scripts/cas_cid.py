import os
import xlrd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'yatcm.settings')
import django
django.setup()
from compounds.models import *  #NOQA
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


structure_file = "/home/jianping/workspace/hz_work_home/data/data_base_result/34680_last_compound.xlsx"


def get_cas_number(cas_cell):
    if cas_cell:
        return cas_cell.split("\n")
    else:
        return []


def get_cid_number(cid_cell):
    if cid_cell:
        return [int(float(cid)) for cid in cid_cell.split("\n")]
    else:
        return []


def upload_cas(row):
    cass = get_cas_number(row[4])
    smiles = row[5].strip()
    for cas in cass:
        if cas:
            print cas
            c, created = CAS.objects.get_or_create(
                cas=cas
            )
            if c:
                compound = Compound.objects.get(smiles=smiles)
                c.compound = compound
                c.save()


def upload_cid(row):
    cids = get_cid_number(row[6])
    smiles = row[5].strip()
    for cid in cids:
        if cid:
            c, created = CID.objects.get_or_create(
                cid=cid
            )
            if c:
                compound = Compound.objects.get(smiles=smiles)
                c.compound = compound
                c.save()


def upload(file_name):
    table = xlrd.open_workbook(file_name).sheet_by_index(0)
    nrows = table.nrows
    for row_number in range(1, nrows):
        row = table.row_values(row_number)
        upload_cas(row)
        # upload_cid(row)

if __name__ == '__main__':
    upload(structure_file)