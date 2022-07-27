import json

from django.db.models import Count
from django.contrib import admin
from django.core.cache import cache

from analaytics.models import Visitor

@admin.register(Visitor)
class VistorAdmin(admin.ModelAdmin):
    
    def changelist_view(self, request, extra_context=None):

        # check if we have a cache
        if cache.get('visitors_count'):
            statstic_data = cache.get('visitors_count')
        else:
            statstic_data = Visitor.objects.values('os').annotate(count=Count('os'))
            cache.set('visitors_count', statstic_data, 60 * 15)

        extra_context = extra_context or {}

        stat_label = []
        stat_data = []
        for stat in statstic_data:
            stat_label.append(stat['os'])
            stat_data.append(stat['count'])

        extra_context['stat_label'] = json.dumps(stat_label)
        extra_context['stat_data'] = json.dumps(stat_data)

        return super().changelist_view(request, extra_context=extra_context)
