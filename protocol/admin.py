from django.contrib import admin
from .models import Claim, Attendance


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    readonly_fields = ['datetime']
    fields = ['team', 'name', 'event', 'played']
    list_display = ['datetime', 'team_name', 'event', 'played']



admin.site.register(Attendance)