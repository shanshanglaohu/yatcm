from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .api import *  # NOQA
from .views import *  # NOQA

router = DefaultRouter()
router.register(r"identity/en", EnglishIdentityViewSet)
router.register(r"identity/ch", ChineseIdentityViewSet)
router.register(r'compounds', CompoundViewSet)
# router.register(r'structures', StructureViewSet)
router.register(r'herbs', HerbViewSet)
router.register(r'cids', CIDViewSet)
router.register(r'cass', CASViewSet)
router.register(r'chembls', ChEMBLViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'keggcompounds', KEGGCompoundViewSet)
router.register(r'keggpathways', KEGGPathwayViewSet)
router.register(r'keggpathwaycategories', KEGGPathwayCategoryViewSet)
router.register(r'keggsimilarities', KEGGSimilarityViewSet)
router.register(r'taxonomies', TCMTaxonomyViewSet)
apiurls = router.urls

compounds_urls = [
    url(r"^(?P<pk>\d+)/detail/$", CompoundDetailView.as_view(), name="compound_detail"),
    url(
        r"^(?P<pk>\d+)/related-compounds$",
        CompoundRelatedCompoundsListView.as_view(),
        name="compound_related_compounds"
    ),
    url(
        r'^(?P<pk>\d+)/related-herbs$',
        CompoundRelatedHerbsListView.as_view(),
        name="compound_related_herbs"
    ),
]

herb_urls = [
    url(r'^(?P<pk>\d+)/detail/$', HerbDetailView.as_view(), name="herb_detail"),
    url(
        r'^(?P<pk>\d+)/related-compounds$',
        HerbRelatedCompoundsView.as_view(),
        name='herb_related_compounds'
        ),
    url(
        r'^(?P<pk>\d+)/related-prescription$',
        HerbRelatedPrescriptionView.as_view(),
        name='herb_related_prescription'
        ),

]


prescription_urls = [
    url(r'^(?P<pk>\d+)/detail/$', PrescriptionDetailView.as_view(), name='prescription_detail'),
]

search_url = [
    url(r'^$', SearchView.as_view(), name='search'),

    url(r'^structure/$', StructureSearchView.as_view(), name='structure-search'),
    url(r'^identify/$', IdentifySearchView.as_view(), name='identify-search'),
]

# url config
urlpatterns = [
    url(r"^api/", include(apiurls)),

    url(r'^search/', include(search_url)),
    # compounds
    url(r"compounds/", include(compounds_urls)),

    # herbs
    url(r"^herbs/", include(herb_urls)),

    # prescription
    url(r'^prescription/', include(prescription_urls)),
]



