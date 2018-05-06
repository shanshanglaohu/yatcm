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
    filename="/home/jianping/workspace/hz_work_home/logs/herb_log.txt",
    filemode='w'
)


def herb_upload(row_number):
    row = table.row_values(row_number)
    cn_name = row[1].strip()
    phonetic_name = row[2].strip()
    en_name = row[3].strip()
    medicinal_part = row[4].strip() if row[5].strip() != 'None' else ''
    wiki_chinese = row[11].strip()
    wiki_link = row[9].strip() if row[9].strip() else row[10].strip()
    image_url = row[13].strip()
    herb, created = Herb.objects.get_or_create(
        name=en_name,
        phonetic_name=phonetic_name,
        chinese_name=cn_name,
        medicinal_part=medicinal_part,
        wiki_chinese=wiki_chinese,
        wiki_link=wiki_link,
        image_url=image_url
    )
    if row[5]:
        tax_id = row[5]
    else:
        tax_id = row[7]

    if tax_id and tax_id != 'None':
        try:
            tax_id = int(float(tax_id))
            print tax_id
            try:
                taxonomy = TCMTaxonomy.objects.get(taxonomy_id=tax_id)
                herb.taxonomy = taxonomy
                herb.save()
            except ObjectDoesNotExist:
                logging.warning("Can not find {} in database".format(tax_id))
            except MultipleObjectsReturned:
                logging.critical("Multiple taxonomy with ID {} find in database".format(tax_id))
        except ValueError:
            logging.debug("{} can not convert to integer".format(tax_id))


if __name__ == '__main__':
    herb_file = "/home/jianping/workspace/hz_work_home/data/data_base_result/7629_vital_source.xlsx"
    table = xlrd.open_workbook(herb_file).sheet_by_index(0)
    nrows = table.nrows
    # pool = multiprocessing.Pool(processes=CORES)
    # pool.map(herb_upload, range(1, nrows))
    map(herb_upload, range(6600, nrows))
    print 'Done!!!'
