from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(EnglishIdentity)
class EnglishIdentityAdmin(admin.ModelAdmin):
    pass


@admin.register(ChineseIdentity)
class ChineseIdentityAdmin(admin.ModelAdmin):
    pass


class EnglishIdentityInline(admin.TabularInline):
    model = EnglishIdentity


class ChineseIdentityInline(admin.TabularInline):
    model = ChineseIdentity


class CIDInline(admin.TabularInline):
    model = CID


class CASIline(admin.TabularInline):
    model = CAS


@admin.register(Compound)
class CompoundAdmin(admin.ModelAdmin):
    search_fields = (
        "english_name",
        "chinese_name"
    )
    inlines = [
        EnglishIdentityInline,
        ChineseIdentityInline,
        CIDInline,
        CASIline
    ]
    exclude = [
        'mol_block',
        'mol',
        "related_compounds",
        'bfp'
    ]

#
# @admin.register(Structure)
# class StructureAdmin(admin.ModelAdmin):
#     pass


@admin.register(Herb)
class HerbAdmin(admin.ModelAdmin):
    filter_horizontal = ['compounds']
    search_fields = (
        "name",
        "chinese_name"
    )


@admin.register(CID)
class CIDAdmin(admin.ModelAdmin):
    search_fields = ("cid",)


@admin.register(CAS)
class CASAdmin(admin.ModelAdmin):
    search_fields = ("cas",)


@admin.register(ChEMBL)
class ChEMBLAdmin(admin.ModelAdmin):
    search_fields = ("chembl_id",)


@admin.register(TCMTaxonomy)
class TCMTaxonomyAdmin(admin.ModelAdmin):
    search_fields = ('name', 'taxonomy_id',)


@admin.register(KEGGCompound)
class KEGGCompoundAdmin(admin.ModelAdmin):
    pass


@admin.register(KEGGPathway)
class KEGGPathwayAdmin(admin.ModelAdmin):
    pass


@admin.register(KEGGPathwayCategory)
class KEGGPathwayCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(KEGGSimilarity)
class KEGGSimilarityAdmin(admin.ModelAdmin):
    pass


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    pass
