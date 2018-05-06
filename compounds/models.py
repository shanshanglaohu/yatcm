from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.core.files import File

from mptt.models import TreeForeignKey, MPTTModel
from django_rdkit.models.fields import *
from django_rdkit.models import *
from django_rdkit.config import config
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem.Crippen import MolLogP
from rdkit.Chem.Lipinski import NumHAcceptors, NumHDonors, NumRotatableBonds

import urllib2
from django.core.files.storage import get_storage_class
import itertools as it
import xml.etree.cElementTree as et


# Create your models here.

__all__ = [
    "Compound", "ChEMBL", "CAS", "CID",
    "TCMTaxonomy", "KEGGSimilarity", "KEGGPathwayCategory",
    "KEGGCompound", "KEGGPathway", 'Herb', 'Prescription',
    'EnglishIdentity', 'ChineseIdentity',
]


class Identity(models.Model):
    identity = models.CharField(max_length=1024)
    compound = models.ForeignKey(
        "Compound", on_delete=models.CASCADE, null=True, blank=True,
        # related_name="%(class)s_related_compound"
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class EnglishIdentity(Identity):
    def __str__(self):
        return self.identity


@python_2_unicode_compatible
class ChineseIdentity(Identity):
    pinyin = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        return self.identity


# @python_2_unicode_compatible
# class Compound(models.Model):
    """
    store basic information of compound.
    """
    # english_name = models.CharField(max_length=1024, blank=True)
    # chinese_name = models.CharField(max_length=1024, blank=True)
    # phonetic_name = models.CharField(max_length=1024, blank=True)
    # synonyms = models.CharField(max_length=1024, blank=True)
    # describe = models.TextField(blank=True)

    # @property
    # def english_name(self):
    #     return self.englishidentity_set.all()[0] or ""
    #
    # @property
    # def chinese_name(self):
    #     return self.chineseidentity_set.all()[0] or ""
    #
    # def __str__(self):
    #     return '{}'.format(self.english_name.indentity)


@python_2_unicode_compatible
class Compound(models.Model):
    """
    store the structure information.
    """
    english_name = models.CharField(max_length=1024, blank=True)
    chinese_name = models.CharField(max_length=1024, blank=True)
    # synonyms = models.CharField(max_length=1024, blank=True)

    smiles = models.CharField(max_length=1024, blank=True)
    mol = MolField(null=True, blank=True)
    mol_block = models.TextField(blank=True)
    bfp = BfpField(blank=True, null=True)
    mol_file = models.FileField(upload_to='mol_files/', blank=True, null=True)
    mol_image = models.ImageField(upload_to='mol_images/', blank=True, null=True)

    related_compounds = models.ManyToManyField(
        'self', blank=True
    )

    first_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # compound's calculated values
    formula = models.CharField(max_length=1024, blank=True)
    mol_weight = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    alogp = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_('Calculated ALogP'),
        blank=True,
        null=True
    )
    hba = models.SmallIntegerField(
        verbose_name=_('Number hydrogen bond acceptors'),
        blank=True,
        null=True,
    )
    hbd = models.SmallIntegerField(
        verbose_name=_('Number hydrogen bond donors'),
        blank=True,
        null=True
    )
    psa = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_('Polar surface area'),
        blank=True,
        null=True
    )
    rtb = models.SmallIntegerField(
        verbose_name=_('Number rotatable bonds'),
        blank=True,
        null=True
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        smiles = self.smiles
        if smiles:
            try:
                self.mol = Chem.MolFromSmiles(smiles)
                self.mol_block = Chem.MolToMolBlock(self.mol)
                self.mol_weight = Descriptors.ExactMolWt(self.mol)
                self.alogp = MolLogP(self.mol)
                self.hba = NumHAcceptors(self.mol)
                self.hbd = NumHDonors(self.mol)
                self.psa = Chem.MolSurf.TPSA(self.mol)
                self.rtb = NumRotatableBonds(self.mol)

                super(Compound, self).save(*args, **kwargs)
                self.formula = Chem.rdMolDescriptors.CalcMolFormula(self.mol)
                self.bfp = MORGANBV_FP(Value(smiles))
            except (ValueError, TypeError):
                print "Error when storing mol object"
                pass
        super(Compound, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.english_name or self.chinese_name or self.pk)

    def get_absolute_url(self):
        return reverse("compound_detail", args=[self.pk])

    def get_kegg_pathways(self):
        li = list(set(it.chain.from_iterable([x.pathway.all() for x in self.keggcompound_set.all()])))
        return li

    class Meta:
        ordering = ['pk']


@python_2_unicode_compatible
class Herb(models.Model):
    name = models.CharField(max_length=1024, blank=True)
    chinese_name = models.CharField(max_length=1024, blank=True)
    phonetic_name = models.CharField(max_length=1024, blank=True)
    describe = models.TextField(blank=True)
    medicinal_part = models.CharField(max_length=1024, blank=True)
    image = models.ImageField(upload_to='herb_images/', blank=True, null=True)
    image_url = models.URLField(blank=True, max_length=2048)
    compounds = models.ManyToManyField('Compound', blank=True)
    wiki_link = models.URLField(blank=True)
    wiki_chinese = models.URLField(blank=True)
    taxonomy = models.ForeignKey('TCMTaxonomy', blank=True, on_delete=models.CASCADE, null=True)

    related_herbs = models.ManyToManyField("self", blank=True)

    def get_absolute_url(self):
        return reverse("herb_detail", args=[self.pk])

    def __str__(self):
        return self.name or self.chinese_name

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     if self.image_url:
    #         wiki_image = urllib2.urlopen(self.image_url)
    #         img = File(wiki_image)
    #         ima_name = '{}.jpg'.format(self.pk)
    #         self.img.save(ima_name, img)
    #     super(Herb, self).save()


@python_2_unicode_compatible
class Prescription(models.Model):
    english_name = models.CharField(max_length=1024, blank=True)
    chinese_name = models.CharField(max_length=1024, blank=True)
    phonetic_name = models.CharField(max_length=1024, blank=True)
    zucheng = models.TextField(blank=True)
    yongfa = models.TextField(blank=True)
    fangjie = models.TextField(blank=True)
    tradition_usage = models.TextField(blank=True)
    modern_usage = models.TextField(blank=True)
    modern_usage_en = models.TextField(blank=True)

    main_prescription = models.ForeignKey("self", blank=True, null=True, on_delete=CASCADE)
    herbs = models.ManyToManyField(Herb)

    def get_absolute_url(self):
        return reverse("prescription_detail", args=[self.pk])

    def __str__(self):
        return '{}'.format(self.english_name or self.chinese_name or self.pk)


@python_2_unicode_compatible
class CAS(models.Model):
    cas = models.CharField(
        _("CAS Registry Number"),
        max_length=1024,
        blank=True, null=True
    )
    url = models.URLField(
        _('URL link to chemfinder database.'),
        blank=True,
        max_length=1024
    )

    compound = models.ForeignKey(Compound, related_name="cas", on_delete=CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = _('CAS')

    def __str__(self):
        return self.cas


@python_2_unicode_compatible
class ChEMBL(models.Model):
    chembl_id = models.CharField(
        _("ChEMBL ID"),
        max_length=1024,
        blank=True,
        null=True,
    )
    url = models.URLField(
        _("URL link to ChEMBL database."),
        blank=True,
        max_length=1024
    )
    compound = models.ForeignKey(Compound, related_name='chembl', on_delete=CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = _("ChEMBL ID")

    def __str__(self):
        return str(self.chembl_id)
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.url = "https://www.ebi.ac.uk/chembl/compound/inspect/{}".format(self.chembl_id)
        super(ChEMBL, self).save()


@python_2_unicode_compatible
class CID(models.Model):
    cid = models.BigIntegerField(
        _("PubChem Compound Identification"),
        blank=True,
        null=True,
    )
    url = models.URLField(
        _("URL link to PubChem."),
        blank=True,
        max_length=1024
    )

    compound = models.ForeignKey(Compound, related_name='cid', on_delete=CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = _('CID')

    def __str__(self):
        return str(self.cid)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.url = 'https://pubchem.ncbi.nlm.nih.gov/compound/%s' % self.cid
        super(CID, self).save()


@python_2_unicode_compatible
class TCMTaxonomy(MPTTModel):
    name = models.CharField(max_length=1024, blank=True)
    # unique_name = models.CharField(max_length=1024, blank=True)
    chinese_name = models.CharField(max_length=1024, blank=True)
    phonetic_name = models.CharField(max_length=1024, blank=True)
    taxonomy_id = models.BigIntegerField(blank=True, null=True)
    # name_class = models.CharField(max_length=1024, blank=True)
    ncbi_link = models.URLField(blank=True)

    parent = TreeForeignKey(
        'self', related_name='children', db_index=True, blank=True, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.ncbi_link = self._get_url(self.taxonomy_id)
        super(TCMTaxonomy, self).save()

    @staticmethod
    def _get_url(taxonomy_id):
        return 'http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=%s' % taxonomy_id


# KEGG pathway

class OverwirteStorage(get_storage_class()):
    def _save(self, name, content):
        self.delet(name)
        return super(OverwirteStorage, self)._save(name, content)

    def get_availabel_name(self, name):
        return name


@python_2_unicode_compatible
class KEGGPathwayCategory(MPTTModel):
    name = models.CharField(max_length=128)
    parent = TreeForeignKey('self', related_name='children', db_index=True, blank=True, null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class KEGGPathway(models.Model):
    kegg_id = models.CharField('KEGG ID', max_length=64)
    name = models.CharField(max_length=128)
    kgml = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='kegg_pathway_image/', storage=OverwirteStorage, blank=True, null=True)
    category = models.ForeignKey(KEGGPathwayCategory, null=True)

    def __str__(self):
        return self.name

    def update_kegg_kgml(self):
        '''
        get kgml content of this pathway from KEGG using KEGG api
        :return:
        '''
        try:
            self.kgml = urllib2.urlopen('http://rest.kegg.jp/get/ko%s/kgml' % self.kegg_id[3:]).read()
            self.save()
        except:
            # todo error exception
            print 'failed to get kgml file'

    def get_kegg_url(self):
        return 'http://www.kegg.jp/kegg-bin/show_pathway?%s' % self.kegg_id

    def get_kegg_image(self):
        """
        get pathway img from KEGG using KEGG API
        :return:
        """
        return 'http://rest.kegg.jp/get/%s/img' % self.kegg_id

    def kgml_parser(self, kegg_cpd_id_list):
        """
        return the mapping data of the pathway, compounds specified by cpd_list
        will be hilighted.
        :param kegg_cpd_id_list: kegg compound list (kegg_id)
        :return:
        """
        result_dic = dict()
        # try:
        kg_tree = et.fromstring(self.kgml)
        for cpd in kegg_cpd_id_list:
            for el in kg_tree.iterfind('entry/graphics[@name="%s"]' % cpd):
                if cpd not in result_dic.keys():
                    result_dic[cpd] = [(el.get('x'), el.get('y'))]
                else:
                    result_dic[cpd].append((el.get('x'), el.get('y')))
        # except:
        #     # todo error exception
        #     print 'error while parsing kgml of %s' % self.kegg_id
        return result_dic


class KEGGCompoundManager(models.Manager):
    def update_similarity_mapping(self):
        # todo update similarity mapping table
        pass


@python_2_unicode_compatible
class KEGGCompound(models.Model):
    kegg_id = models.CharField('KEGG ID', max_length=64)
    name = models.CharField(max_length=256, blank=True, null=True)
    mol = MolField(verbose_name=_('An RDKit molecule'), null=True, blank=True)
    mol_block = models.TextField(_('Mol block'), blank=True, null=True)
    smiles = models.TextField(max_length=1024, blank=True, null=True)
    mol_image = models.ImageField(upload_to='mol_image/', storage=OverwirteStorage, blank=True, null=True)
    pathway = models.ManyToManyField(KEGGPathway)
    similar_to_tcm = models.ManyToManyField(Compound, through='KEGGSimilarity')

    objects = KEGGCompoundManager()

    def __str__(self):
        return self.name or self.kegg_id

    def refresh_similarity_to_tcm(self, threshold=0.8):
        """
        refresh the similarity mapping to TCM of this compounds
        :return: None
        """

        config.tanimoto_threshold = threshold
        value = MORGANBV_FP(Value(self.smiles))
        self.similar_to_tcm.clear()
        try:
            for obj in Compound.objects.filter(bfp__tanimoto=value):
                tcm_cpd = obj.compound
                if not self.similar_to_tcm.filter(id=tcm_cpd.id).exists():
                    similarity = KEGGSimilarity.objects.create(
                        tcm=tcm_cpd,
                        kegg_compound=self  # todo: similarity value
                    )
                    similarity.save()
            self.save()
        except:  # todo invalide molecular exception
            print 'invalid smiles : %s , %s' % (self.id, self.smiles)


class KEGGSimilarity(models.Model):
    tcm = models.ForeignKey(Compound)
    kegg_compound = models.ForeignKey(KEGGCompound)
    similarity = models.FloatField(blank=True, null=True)


# target


# disease
