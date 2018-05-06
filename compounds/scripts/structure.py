import os
import xlrd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'yatcm.settings')
import django
django.setup()
from compounds.models import *  #NOQA
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


structure_file = "/home/jianping/workspace/hz_work_home/data/data_base_result/34680_last_compound.xlsx"


def extract_smiles(cell):
    return cell.strip()


def extract_herbs(cell):
    return cell.split("\n")


def upload_structure(row):
    smiles = extract_smiles(row[5])
    # st, created = Structure.objects.get_or_create(smiles=smiles)
    compound, created = Compound.objects.get_or_create(structure__smiles=smiles)
    herbs_en = extract_herbs(row[7])
    herbs_cn = extract_herbs(row[8])
    if compound:
        for herb_en in herbs_en:
            herbs = Herb.objects.filter(name=herb_en)
            for herb in herbs:
                compound.herb_set.add(herb)
                compound.save()

        for herb_cn in herbs_cn:
            herbs = Herb.objects.filter(chinese_name=herb_cn)
            # compound.herb_set.bulk_create(herbs)
            for herb in herbs:
                compound.herb_set.add(herb)
                compound.save()


def upload(file_name):
    table = xlrd.open_workbook(file_name).sheet_by_index(0)
    nrows = table.nrows
    for row_number in range(1, nrows):
        row = table.row_values(row_number)
        upload_structure(row)

if __name__ == '__main__':
    upload(structure_file)