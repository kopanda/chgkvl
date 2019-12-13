from django.contrib import admin
from .models import Tournament, Person, Team
from datetime import datetime


class DateFilter(admin.SimpleListFilter):
    title = 'Даты'
    parameter_name = 'dates'

    def lookups(self, request, model_admin):
        return (
            ('past', 'Уже закончились'),
            ('present', 'Идут сейчас'),
            ('future', 'Ещё не начались'),
            ('present-future', 'Идут сейчас и ещё не начались'),
        )

    def queryset(self, request, queryset):
        n = datetime.now()
        if self.value() == 'past':
            return queryset.filter(date_end__lt=n)
        elif self.value() == 'present':
            return queryset.filter(date_start__lte=n, date_end__gte=n)
        elif self.value() == 'future':
            return queryset.filter(date_start__gt=n)
        elif self.value() == 'present-future':
            return queryset.filter(date_end__gte=n)


class TypeFilter(admin.SimpleListFilter):
    title = 'Типы'
    parameter_name = 'types'

    def lookups(self, request, model_admin):
        return (
            ('s', 'Синхрон, асинхрон'),
            ('f', 'Очный, региональный, марафон'),
            ('d', 'Остальное'),
        )

    def queryset(self, request, queryset):
        if self.value() == 's':
            return queryset.filter(type_name='Синхрон') | queryset.filter(type_name='Асинхрон') | queryset.filter(
                type_name='Строго синхроный')
        elif self.value() == 'f':
            return queryset.filter(type_name='Обычный') | queryset.filter(type_name='Региональный') | queryset.filter(
                type_name='Марафон')
        elif self.value() == 'd':
            return queryset.filter(type_name='Неизвестный') | queryset.filter(
                type_name='Общий зачёт') | queryset.filter(type_name='-') | queryset.filter(type_name=None)


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name', 'long_name',
                ('tournament_in_rating', 'type_name', 'town', 'archive'),
                ('date_start', 'date_end', 'date_requests_allowed_to', 'date_archived_at'),
                ('tour_count', 'tour_questions', 'tour_ques_per_tour', 'questions_total'),
                ('main_payment_value', 'main_payment_currency'),
                ('discounted_payment_value', 'discounted_payment_currency'),
                'discounted_payment_reason',
                'comment',
                'db_tags',
                'orgcommittee',
                'authors',
                'game_jury',
                'jury_of_appeal',

            )
        }),
    )
    readonly_fields = [
        "name",
        "town",
        "long_name",
        "date_start",
        "date_end",
        "tour_count",
        "tour_questions",
        "tour_ques_per_tour",
        "questions_total",
        "type_name",
        "main_payment_value",
        "main_payment_currency",
        "discounted_payment_value",
        "discounted_payment_currency",
        "discounted_payment_reason",
        "tournament_in_rating",
        "date_requests_allowed_to",
        "comment",
        "archive",
        "date_archived_at",
        "db_tags",
        "json",
        "orgcommittee",
        "authors",
        "game_jury",
        "jury_of_appeal",
    ]
    list_display = ['name', 'id', 'date_start', 'date_end', 'type_name']
    list_display_links = ['name', 'id']
    list_filter = [TypeFilter, DateFilter, 'archive']


class JsonFilter(admin.SimpleListFilter):
    title = 'JSON'
    parameter_name = 'json'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Загружен'),
            ('no', 'Не загружен'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(json__isnull=False)
        else:
            return queryset.filter(json=None)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = [
        "comment",
        "db_chgk_info_tag",
        "json",
    ]
    list_display = ['id', 'surname', 'name', 'patronymic', 'json_exist']
    list_filter = ['town', JsonFilter]
    empty_value_display = '— пусто —'

    def json_exist(self, obj):
        return not (obj.json is None)

    json_exist.boolean = True


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    readonly_fields = [
        "name",
        "town",
        "region_name",
        "country_name",
        "tournaments_this_season",
        "tournaments_total",
        "comment",
    ]
