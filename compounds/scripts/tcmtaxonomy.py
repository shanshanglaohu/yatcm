import os
import xlrd
import re
import multiprocessing
import time
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'yatcm.settings')
import django
django.setup()
from compounds.models import *  #NOQA
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import pandas as pd

CORES = multiprocessing.cpu_count()
names_file = '/home/jianping/workspace/hz_work_home/data/taxdump/names.dmp'
nodes_file = '/home/jianping/workspace/hz_work_home/data/taxdump/nodes.dmp'
herb_file = '/home/jianping/workspace/hz_work_home/data/data_base_result/all_compound_add_remained_tw_1.xlsx'
taxonomy_file = "/home/jianping/workspace/hz_work_home/data/data_base_result/taxonomy_new.txt"


logger = logging.getLogger("tax_logger")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("/home/jianping/workspace/hz_work_home/logs/tax_log.txt")
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
"""
   upload the taxonomy by re
"""


"""
def file_to_string(file_name):
    "read the dmp file and convert it to a String"
    rows = open(file_name).readlines()
    file_string = ''.join(rows)
    return file_string


def find_scientific_name(tax_id, names_string):
    name_regex = re.compile(r'%s\t\|\t.*scientific name\t\|\n' % tax_id)
    m = name_regex.search(names_string)
    if m:
        return m.group()
    else:
        return None


def find_parent_node(tax_id, nodes_string):
    node_regex = re.compile(r'%s\t\|\t\d+?.*?\t\|\n' % tax_id)
    m = node_regex.search(nodes_string)
    if m:
        return m.group()
    else:
        return None


def get_parent_id(node_string):
    parent_id = node_string.split('\t|\t')[1]
    try:
        parent_id = int(parent_id)
        return parent_id
    except ValueError:
        return None


def node_save(tax_id, names_string):
    name_string = find_scientific_name(tax_id, names_string)
    # print name_string
    if name_string:
        try:
            tax_id, name, unique_name, name_class = name_string.split('\t|\t')
        except ValueError:
            tax_id, name, name_class = name_string.split('\t|\t')
            unique_name = ''
        tax_id = int(tax_id)
        name_class = name_class[:-3]
        taxonomy, created = TCMTaxonomy.objects.get_or_create(
            taxonomy_id=tax_id,
            name=name,
            unique_name=unique_name,
            name_class=name_class

        )
        return taxonomy, created
    else:
        return None, None


def taxonomy_upload(table, row_number):
    row = table.row_values(row_number)
    tax_id = None
    if row[6] != 'None':
        tax_id = row[6]
    elif row[8] != 'None':
        tax_id = row[8]

    if tax_id and tax_id != 'None':
        tax_id = int(float(tax_id))
        famliy_ids = [tax_id]
        tmp = tax_id
        while 1:
            parent_node = find_parent_node(tmp, nodes_string)
            parent_id = get_parent_id(parent_node)
            famliy_ids.append(parent_id)
            tmp = parent_id
            if 1 in famliy_ids:
                print famliy_ids
                break
        parent = None

        for taxonomy_id in famliy_ids[::-1]:
            taxonomy, created = node_save(taxonomy_id, names_string)
            if parent and created:
                taxonomy.parent = parent
                taxonomy.save()
            parent = taxonomy
            # try:
            #     taxonomy = TCMTaxonomy.objects.get(taxonomy_id=taxonomy_id)
            #     if taxonomy:
            #         return
            # except TCMTaxonomy.DoesNotExist:
            #     taxonomy, created = node_save(taxonomy_id, names_string)
            #     if taxonomy_tmp:
            #         taxonomy_tmp.parent = taxonomy
            #         taxonomy_tmp.save()
            #     taxonomy_tmp = taxonomy
            # except MultipleObjectsReturned:
            #     f = open("/home/jianping/Desktop/log.txt", 'a+')
            #     f.write(str(taxonomy_id))
            #     f.write('/n')
            #     f.close()


if __name__ == '__main__':
    names_string = file_to_string(names_file)
    nodes_string = file_to_string(nodes_file)
    table = xlrd.open_workbook(herb_file).sheet_by_index(0)
    nrows = table.nrows
    # pool = multiprocessing.Pool(processes=CORES)
    # pool.map(taxonomy_upload, range(1, nrows))
    map(taxonomy_upload, range(1, nrows))
"""


# """
# Try to rewrite the upload script using Thread
# """
#
#
# class HerbThread(Thread):
#     def __init__(self, table, row_number):
#         super(HerbThread, self).__init__()
#         self.table = table
#         self.row_number = row_number
#
#     def run(self):
#         taxonomy_upload(self.table, self.row_number)


""" upload taxonomy using pandas """


def get_tax(file_name):
    with open(file_name) as f:
        for row in f:
            yield int(row.strip())


def get_sci_name(names_data, node):
    return names_data[(names_data[0] == node) & (names_data[3] == "scientific name")].iloc[0][1]


def get_parent_id(nodes_data, node):
    return nodes_data[nodes_data[0] == node].iloc[0][1]


def get_family(nodes_data, child_node):
    family = [child_node]
    while family[-1] != 1:
        family.append(get_parent_id(nodes_data, child_node))
        child_node = get_parent_id(nodes_data, child_node)
    return family


if __name__ == '__main__':
    start = time.clock()
    nodes = pd.read_table(nodes_file, header=None, sep=r"\t\|\t", usecols=range(12))
    read_nodes = time.clock()
    logger.info("read nodes spent {} s".format(read_nodes-start))  # calculate times

    names = pd.read_table(names_file, header=None, sep="\t\|\t|\t\|", usecols=range(4))
    read_names = time.clock()
    logger.info("read names spent {} s".format(read_names - read_nodes))

    taxonomies = get_tax(taxonomy_file)

    for tax in taxonomies:

        # start = time.clock()
        try:
            family = get_family(nodes, tax)
        except IndexError:
            logger.warning("{} get no data form database".format(tax))
            continue
        child = None
        for node in family:
            try:
                name = get_sci_name(names, node)
                taxonomy, created = TCMTaxonomy.objects.get_or_create(name=name, taxonomy_id=node)
                if child:
                    child.parent = taxonomy
                    child.save()
                child = taxonomy
                if not created:
                    break
            except TCMTaxonomy.MultipleObjectsReturned:
                logger.warning("{} returns more than one recodes.".format(node))
        # end = time.clock()
        # logger.info("{}s spent per loop".format(end-start))