import django_filters


class ItemFilter(django_filters.FilterSet):
    no_owner = django_filters.BooleanFilter(field_name='owner', lookup_expr='isnull')
    owner = django_filters.AllValuesFilter(field_name="owner")