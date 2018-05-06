import os
import xlrd
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'yatcm.settings')
import django
django.setup()
from compounds.models import *  #NOQA
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


primary_file = "/home/jianping/workspace/hz_work_home/data/data_base_result/primary_prescription.xlsx"
vice_file = "/home/jianping/workspace/hz_work_home/data/data_base_result/vice_prescription.xlsx"


logger = logging.getLogger("tax_logger")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("/home/jianping/workspace/hz_work_home/logs/prescription_log.txt")
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def primary_upload(row):
    chinese_name = row[0].strip()
    zucheng = row[1].strip()
    herb_list = row[2].strip().split()
    yongfa = row[3].strip()
    fangjie = row[5].strip()
    tradition_usage = row[4].strip()
    modern_usage = row[6].strip()
    modern_usage_en = row[7].strip()

    try:
        prescription, created = Prescription.objects.get_or_create(
            chinese_name=chinese_name,
            zucheng=zucheng,
            yongfa=yongfa,
            fangjie=fangjie,
            tradition_usage=tradition_usage,
            modern_usage=modern_usage,
            modern_usage_en=modern_usage_en
        )
    except Prescription.DoesNotExist:
        logger.warning("{} dose not exist!".format(unicode(chinese_name)))
    except Prescription.MultipleObjectsReturned:
        logger.warning("{} return more than one objects".format(unicode(chinese_name)))

    for herb_name in herb_list:
        try:
            herbs = Herb.objects.filter(chinese_name=herb_name)
            for herb in herbs:
                prescription.herbs.add(herb)
                prescription.save()
        except Herb.DoesNotExist:
            logger.info("{} dose not exist".format(herb_name))


def vice_upload(row):
    main_prescription_name = row[0].strip()
    chinese_name = row[1].strip()
    zucheng = row[3].strip()
    yongfa = row[2].strip()
    herb_list = row[3].strip().split()
    try:
        prescription, created = Prescription.objects.get_or_create(
            chinese_name=chinese_name,
            zucheng=zucheng,
            yongfa=yongfa,
        )
        try:
            main_prescription = Prescription.objects.get(chinese_name=main_prescription_name)
            prescription.main_prescription = main_prescription
            prescription.save()
        except Prescription.DoesNotExist:
            logger.warning("%s dose not exist!" % main_prescription_name)
        except Prescription.MultipleObjectsReturned:
            logger.warning("%s return more than one objects" % main_prescription_name)
        for herb_name in herb_list:
            try:
                herbs = Herb.objects.filter(chinese_name=herb_name)
                for herb in herbs:
                    prescription.herbs.add(herb)
                    prescription.save()
            except Herb.DoesNotExist:
                logger.info("{} dose not exist".format(herb_name))

    except Prescription.DoesNotExist:
        logger.warning("%s dose not exist!" % chinese_name)
    except Prescription.MultipleObjectsReturned:
        logger.warning("%s return more than one objects" % chinese_name)


if __name__ == '__main__':
    primary_table = xlrd.open_workbook(primary_file).sheet_by_index(0)
    for row_number in range(1, primary_table.nrows):
        row = primary_table.row_values(row_number)
        primary_upload(row)

    vice_table = xlrd.open_workbook(vice_file).sheet_by_index(0)
    for row_number in range(1, vice_table.nrows):
        row = vice_table.row_values(row_number)
        vice_upload(row)