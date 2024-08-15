from django_filters import rest_framework as filters

from core.models import Repertoire,PerformanceSeance


class RepertoireFilter(filters.FilterSet):
    created_at = filters.DateRangeFilter()

    class Meta:
        model = Repertoire
        fields = ['genres', 'director']


class PerformanceSeanceFilter(filters.FilterSet):
    date = filters.DateFilter()
    time = filters.TimeFilter()

    class Meta:
        model = PerformanceSeance
        fields = ['date', 'time']