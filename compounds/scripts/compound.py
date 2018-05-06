import os
import xlrd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'yatcm.settings')
import django
django.setup()
from compounds.models import *  #NOQA
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import logging

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s-[%(message)s]",
    filename="/home/jianping/workspace/hz_work_home/logs/compound_log.txt",
    filemode='w'
)


def extract_cids(cell):
    return [int(float(x)) for x in cell.split("\n")] if cell else []


def herbs_extract(cell):
    cell = cell.replace("?", '').strip()
    herbs = cell.split("\n") if cell else []
    for herb in herbs:
        yield herb.split(';')


def upload_compound(row_number):
    row = table.row_values(row_number)
    cn_name = row[0].strip()
    cn_synonyms = row[1].split("\n") if row[1] else []
    en_name = row[2].strip()
    en_synonyms = row[3].split("\n") if row[3] else []
    smiles = row[4].strip()
    herbs = herbs_extract(row[5])
    cids = extract_cids(row[6])
    cass = row[7].split("\n") if row[7] else []

    compound, created = Compound.objects.get_or_create(
        english_name=en_name,
        chinese_name=cn_name,
        smiles=smiles
    )

    for cn_identity in cn_synonyms:
        chinese_identity, created = ChineseIdentity.objects.get_or_create(identity=cn_identity)
        chinese_identity.compound = compound
        chinese_identity.save()

    for en_identity in en_synonyms:
        english_identity, created = EnglishIdentity.objects.get_or_create(identity=en_identity)
        english_identity.compound = compound
        english_identity.save()


    for cid in cids:
        try:
            c, created = CID.objects.get_or_create(cid=cid)
            c.compound = compound
            c.save()
        except CID.DoesNotExist:
            logging.warning("{} Dose not find in CID database".format(cid))
        except CID.MultipleObjectsReturned:
            logging.warning("{} find multiple cid objs in database".format(cid))

    for cas in cass:
        try:
            ca, created = CAS.objects.get_or_create(cas=cas)
            ca.compound = compound
            ca.save()
        except CAS.DoesNotExist:
            logging.debug("{} CAS dose not exist".format(cas))
        except CAS.MultipleObjectsReturned:
            logging.debug("{} return multiple cas objs".format(cas))

    for herb in herbs:
        try:
            h = Herb.objects.get(name=herb[1], chinese_name=herb[0])
            h.compounds.add(compound)
            h.save()
        except Herb.DoesNotExist:
            logging.info("Can not find %s, %s in database" %(herb[0], herb[1]))
        except Herb.MultipleObjectsReturned:
            logging.info("return multiple herbs %s, %s" %(herb[0], herb[1]))


if __name__ == '__main__':
    compound_file = "/home/jianping/workspace/hz_work_home/data/data_base_result/34680_vital_structure.xlsx"
    table = xlrd.open_workbook(compound_file).sheet_by_index(0)
    nrows = table.nrows
    # pool = multiprocessing.Pool(processes=CORES)
    # pool.map(herb_upload, range(1, nrows))
    map(upload_compound, range(1, nrows))
    print 'Done!!!'
