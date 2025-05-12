import re
from datetime import datetime
from django.db.models import Q


def apply_search_filter(request, queryset, fields, param='search'):
    search = request.query_params.get(param, '').strip()
    if not search:
        return queryset
    pattern = r'(^|\s)%s' % re.escape(search)
    q = Q()
    for field in fields:
        q |= Q(**{f"{field}__istartswith": search})
        q |= Q(**{f"{field}__iregex": pattern})
    return queryset.filter(q)

def apply_date_filter(request, queryset, field='date', param='date'):
    date_param = request.query_params.get(param)
    if not date_param:
        return queryset
    try:
        date = datetime.strptime(date_param, '%Y-%m-%d').date()
        return queryset.filter(**{field: date})
    except ValueError:
        return queryset

def apply_bool_filter(request, queryset, field, param=None):
    key = param or field
    val = request.query_params.get(key)
    
    if val is None:
        return queryset
    v = val.lower()
    if v in ['true', '1']:
        return queryset.filter(**{field: True})
    if v in ['false', '0']:
        return queryset.filter(**{field: False})
    
    return queryset
