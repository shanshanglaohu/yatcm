from django.shortcuts import render
from django.shortcuts import HttpResponse
from collections import defaultdict
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import StreamingHttpResponse
from django.core import serializers
from .models import *    #NOQA
from django.views.generic import TemplateView, DetailView, View
from django_rdkit.config import config
from django_rdkit.models import *
from rdkit import Chem
# Create your views here.


__all__ = [
    "SearchView",
    "StructureSearchView",
    "IdentifySearchView",
    "CompoundRelatedCompoundsListView",
    "CompoundDetailView",
    "CompoundRelatedHerbsListView",
    "HerbDetailView",
    'HerbRelatedCompoundsView',
    "HerbRelatedPrescriptionView",
    "PrescriptionDetailView",
]


class SearchView(TemplateView):
    template_name = "search.html"


class StructureSearchView(View):

    def post(self, request):
        if request.is_ajax():
            data = request.POST
            is_sub = data.get("is_sub")
            tanimoto = float(data.get("tanimoto", 0.8))
            smiles = data.get("smiles")
            if is_sub and smiles:
                compounds = self._substructure_search(smiles)
                # paginator = Paginator(compounds, 25)
                respone = render(
                    request, template_name="result/compounds_result.html",
                    context={
                        "compounds": compounds,
                        # "paginator": paginator
                             }
                )
                return StreamingHttpResponse(respone.content)

            elif not is_sub and smiles:
                compounds = self._similarity_search(smiles, tanimoto=tanimoto)
                # paginator = Paginator(compounds, 25)
                response = render(
                    request,
                    template_name="result/result.html",
                    context={
                        "compounds": compounds,
                        # "paginator": paginator
                    }
                )
                return StreamingHttpResponse(response.content)

    @staticmethod
    def _similarity_search(smiles, tanimoto=0.8):
        config.tanimoto_threshold = tanimoto
        value = MORGANBV_FP(Value(smiles))
        compound_list = Compound.objects.filter(
            bfp__tanimoto=value
        )
        return compound_list

    @staticmethod
    def _substructure_search(smiles):
        compound_list = Compound.objects.filter(mol__hassubstruct=QMOL(Value(smiles)))
        return compound_list


class IdentifySearchView(View):

    def post(self, request):
        if request.is_ajax():
            data = request.POST
            type = data.get("type").strip().lower()
            query = data.get("query").strip().lower()
            context = defaultdict()
            if type == "compound" or type == "formula":
                compounds = self._compound_search(query)
                context.setdefault('compounds', compounds)
            elif type == "herb":
                herbs = self._herb_search(query)
                context.setdefault("herbs", herbs)
            elif type == "prescription":
                prescriptions = self._prescription_search(query)
                context.setdefault("prescriptions", prescriptions)
            elif type == "formula":
                compounds = self._formula_search(query)
                context.setdefault("compounds", compounds)
            elif type == "all":
                compounds = self._compound_search(query)
                herbs = self._herb_search(query)
                prescriptions = self._prescription_search(query)
                context.setdefault('compounds', compounds)
                context.setdefault("herbs", herbs)
                context.setdefault("prescriptions", prescriptions)
            return StreamingHttpResponse(render(request, template_name="result/result.html", context=context))

    @staticmethod
    def _compound_search(query):
        compound_list = Compound.objects.filter(
            Q(english_name__icontains=query) |
            Q(chinese_name__icontains=query) |
            Q(formula__iexact=query) |
            Q(englishidentity__identity__icontains=query) |
            Q(chineseidentity__identity__icontains=query) |
            Q(chineseidentity__pinyin__icontains=query)
        )
        return compound_list

    @staticmethod
    def _herb_search(query):
        herb_list = Herb.objects.filter(
            Q(name__icontains=query) |
            Q(chinese_name__icontains=query) |
            Q(phonetic_name__icontains=query)
        )
        return herb_list

    @staticmethod
    def _formula_search(query):
        compound_list = Compound.objects.filter(
            formula__iexact=query
        )
        return compound_list

    @staticmethod
    def _prescription_search(query):
        prescription_list = Prescription.objects.filter(
            Q(chinese_name__icontains=query) |
            Q(english_name__icontains=query) |
            Q(phonetic_name__icontains=query)
        )
        return prescription_list


#
#
# detail pages and list pages
class CompoundDetailView(DetailView):
    model = Compound
    template_name = "compound_detail.html"


class CompoundRelatedCompoundsListView(TemplateView):
    template_name = "compound_list.html"

    def get_context_data(self, **kwargs):
        context = super(CompoundRelatedCompoundsListView, self).get_context_data()
        pk = int(kwargs['pk'])
        compound = Compound.objects.get(pk=pk)
        related_compounds = compound.related_compounds.all()
        context['compounds'] = related_compounds
        return context


class CompoundRelatedHerbsListView(TemplateView):
    template_name = 'herb_list.html'

    def get_context_data(self, **kwargs):
        context = super(CompoundRelatedHerbsListView, self).get_context_data()
        pk = int(kwargs['pk'])
        compound = Compound.objects.get(pk=pk)
        related_herbs = compound.herb_set.all()
        context['herbs'] = related_herbs
        return context


class HerbDetailView(DetailView):
    template_name = "herb_detail.html"
    model = Herb

    def get_context_data(self, **kwargs):
        context = super(HerbDetailView, self).get_context_data()
        herb = self.get_object()
        taxonomy = herb.taxonomy
        if taxonomy:
            taxonomy_list = taxonomy.get_ancestors(include_self=True)
            context['taxonomy_list'] = taxonomy_list
        return context


class HerbRelatedCompoundsView(TemplateView):
    template_name = 'compound_list.html'

    def get_context_data(self, **kwargs):
        context = super(HerbRelatedCompoundsView, self).get_context_data()
        pk = kwargs['pk']
        herb = Herb.objects.get(pk=pk)
        related_compounds = herb.compounds.all()
        context['compounds'] = related_compounds
        return context


class HerbRelatedPrescriptionView(TemplateView):
    template_name = "prescription_list.html"

    def get_context_data(self, **kwargs):
        context = super(HerbRelatedPrescriptionView, self).get_context_data()
        pk = kwargs['pk']
        herb = Herb.objects.get(pk=pk)
        related_prescriptions = herb.prescription_set.all()
        context['prescriptions'] = related_prescriptions
        return context


class PrescriptionDetailView(DetailView):
    template_name = "prescription_detail.html"
    model = Prescription
