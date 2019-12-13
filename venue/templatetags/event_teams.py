from django import template

register = template.Library()


@register.filter
def team_exist(queryset, team):
    return team.idteam in queryset.values_list('team', flat=True)