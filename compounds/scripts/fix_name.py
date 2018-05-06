import os
import xlrd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'yatcm.settings')
import django
django.setup()
from compounds.models import *  #NOQA

fix_file = "/home/jianping/workspace/hz_work_home/data/79_need_to_fix_English_name.xlsx"


def fix_name(row):
    en_name = row[2].strip()
    fixed_en_name = row[7].strip()

    try:
        compound = Compound.objects.get(english_name=en_name)
        compound.english_name = fixed_en_name
        compound.save()
    except Compound.DoesNotExist:
        print "%s can not find in database " % en_name
    except Compound.MultipleObjectsReturned:
        print "%s return more than one objs" % en_name


if __name__ == '__main__':
    table = xlrd.open_workbook(fix_file).sheet_by_index(0)
    nrows = table.nrows
    for i in range(1, nrows):
        row = table.row_values(i)
        fix_name(row)