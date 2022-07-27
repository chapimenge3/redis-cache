import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.contrib import admin

from analaytics.models import Visitor

@admin.register(Visitor)
class VistorAdmin(admin.ModelAdmin):
    
    def changelist_view(self, request, extra_context=None):
        statstic_data = Visitor.objects.values('os').annotate(count=Count('os'))

        extra_context = extra_context or {}

        stat_label = []
        stat_data = []
        for stat in statstic_data:
            stat_label.append(stat['os'])
            stat_data.append(stat['count'])

        extra_context['stat_label'] = json.dumps(stat_label)
        print(stat_label)
        extra_context['stat_data'] = json.dumps(stat_data)

        return super().changelist_view(request, extra_context=extra_context)
