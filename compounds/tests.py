from django.test import TestCase
from .models import *  #NOQA
# Create your tests here.


class TCMTaxonomyTest(TestCase):

    def test_all_taxonomy_root_node_is_root(self):
        taxonomies = TCMTaxonomy.objects.all()
        root = TCMTaxonomy.objects.get(taxonomy_id=1)
        for taxonomy in taxonomies:
            self.assertEqual(
                taxonomy.get_root(),
                root,
                msg="{} failed".format(taxonomy.taxonomy_id)
            )

