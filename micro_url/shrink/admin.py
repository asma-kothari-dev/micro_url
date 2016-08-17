# django imports
from django.contrib import admin

# app imports
from models import  MicroUrl


class MicroUrlAdmin(admin.ModelAdmin):
    fields = ('link', 'alias', 'micro_url',)
    readonly_fields = ('micro_url',)


admin.site.register(MicroUrl, MicroUrlAdmin)
