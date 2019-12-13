from django.db.models import *
import requests
from lxml import etree
from decimal import Decimal
from datetime import datetime
from pytz import timezone
from distutils.util import strtobool

town = "Владивосток"


def get_date(date):
    return "" if date is None else timezone('Europe/Moscow').localize(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))


def safe(default, exception, function, *args):
    try:
        return function(*args)
    except exception:
        return default


def get_by_id(item_id, item_type):
    try:
        if item_type == "player_tournaments":
            return requests.get("https://rating.chgk.info/api/players/%s/tournaments/.json" % item_id).json()
        else: 
            return requests.get("https://rating.chgk.info/api/%s/%s.json" % (item_type, item_id)).json()[0]
    except KeyError:
        return None


def get_by_id_new(item_id, item_type):
    try:
        return requests.get("http://api.rating.chgk.net/%s/%s.json" % (item_type, item_id)).json()
    except KeyError:
        return None


class Season(Model):
    id = PositiveIntegerField(unique=True, primary_key=True)
    date_start = DateTimeField(default=None, null=True, editable=False)
    date_end = DateTimeField(default=None, null=True, editable=False)


class Country(Model):
    id = PositiveIntegerField(unique=True, primary_key=True)
    name = CharField(default="", max_length=100, editable=False)


class Region(Model):
    id = PositiveIntegerField(unique=True, primary_key=True)
    country = ForeignKey(Country, on_delete=CASCADE, related_name="regions")
    name = CharField(default="", max_length=100, editable=False)


class Town(Model):
    id = PositiveIntegerField(unique=True, primary_key=True)
    country = ForeignKey(Country, on_delete=CASCADE, related_name="towns")
    region = ForeignKey(Country, on_delete=CASCADE, related_name="towns")
    name = CharField(default="", max_length=100, editable=False)


class TournamentFlag(Model):
    id = PositiveIntegerField(unique=True, primary_key=True)
    short_name = CharField(default="", max_length=30, editable=False)
    long_name = CharField(default="", max_length=300, editable=False)


class TournamentType(Model):
    id = PositiveIntegerField(unique=True, primary_key=True)
    name = CharField(default="", max_length=100, editable=False)


class Tournament(Model):
    id = PositiveIntegerField(unique=True, primary_key=True)
    name = CharField(default="", max_length=100, editable=False)
    town = CharField(default=None, null=True, max_length=30, editable=False)
    town_id = ForeignKey(Town, on_delete=CASCADE, related_name="tournaments")
    long_name = TextField(default="", null=True, editable=False)
    date_start = DateTimeField(default=None, null=True, editable=False)
    date_end = DateTimeField(default=None, null=True, editable=False)
    season = ForeignKey(Season, on_delete=CASCADE, related_name="tournaments")
    tour_count = PositiveSmallIntegerField(default=None, null=True, editable=False)
    tour_questions = PositiveSmallIntegerField(default=None, null=True, editable=False)
    tour_ques_per_tour = CharField(default=None, null=True, max_length=30, editable=False)
    questions_total = PositiveSmallIntegerField(default=None, null=True, editable=False)
    type_name = CharField(default=None, null=True, max_length=128, editable=False)
    type_id = ForeignKey(TournamentType, on_delete=CASCADE, related_name="tournaments")
    main_payment_value = DecimalField(default=0, max_digits=8, decimal_places=2, editable=False)
    main_payment_currency = CharField(default="", max_length=10, editable=False)
    discounted_payment_value = DecimalField(default=0, max_digits=8, decimal_places=2, editable=False)
    discounted_payment_currency = CharField(default="", null=True, max_length=10, editable=False)
    discounted_payment_reason = TextField(default="", null=True, editable=False)
    tournament_in_rating = BooleanField(default=False, editable=False)
    comment = TextField(default="", null=True, editable=False)
    site_url = CharField(default=None, null=True, max_length=120, editable=False)
    archive = BooleanField(default=False, editable=False)
    db_tags = CharField(default=None, null=True, max_length=120, editable=False)

    date_requests_allowed_to = DateTimeField(null=True, editable=False)
    result_fixes_to = DateTimeField(default=None, null=True, editable=False)
    results_recaps_to = DateTimeField(default=None, null=True, editable=False)
    allow_appeal_cancel = BooleanField(default=False, editable=False)
    allow_narrator_error_appeal = BooleanField(default=False, editable=False)
    date_archived_at = DateTimeField(default=None, null=True, editable=False)
    date_download_questions_from = DateTimeField(default=None, null=True, editable=False)
    date_download_questions_to = DateTimeField(default=None, null=True, editable=False)
    hide_questions_to = DateTimeField(default=None, null=True, editable=False)
    hide_results_to = DateTimeField(default=None, null=True, editable=False)
    all_verdicts_done = DateTimeField(default=None, null=True, editable=False)
    instant_controversial = BooleanField(default=False, editable=False)

    json = TextField(default="", editable=False)
    json_new = TextField(default="", editable=False)

    orgcommittee = ManyToManyField('rating.Person', blank=True, related_name="orgcommittee",
                                   verbose_name="организаторы")
    authors = ManyToManyField('rating.Person', blank=True, related_name="authors",
                              verbose_name="редакторы")
    game_jury = ManyToManyField('rating.Person', blank=True, related_name="game_jury",
                                verbose_name="игровое жюри")
    jury_of_appeal = ManyToManyField('rating.Person', blank=True, related_name="jury_of_appeal",
                                     verbose_name="апелляционное жюри")

    def update(self):
        json = get_by_id(self.id, "tournaments")
        self.json = json
        self.name = json['name']
        self.town = json['town']
        self.long_name = json['long_name']
        self.date_start = get_date(json['date_start'])
        self.date_end = get_date(json['date_end'])
        self.tour_count = int(json['tour_count'])
        self.tour_questions = int(json['tour_questions'])
        self.tour_ques_per_tour = json['tour_ques_per_tour']
        self.questions_total = int(json['questions_total'])
        self.type_name = json['type_name']
        self.main_payment_value = safe(0, TypeError, Decimal, json['main_payment_value'])
        self.main_payment_currency = json['main_payment_currency']
        self.discounted_payment_value = safe(0, TypeError, Decimal, json['discounted_payment_value'])
        self.discounted_payment_currency = json['discounted_payment_currency']
        self.discounted_payment_reason = json['discounted_payment_reason']
        self.tournament_in_rating = bool(int(json['tournament_in_rating']))
        self.date_requests_allowed_to = get_date(json['date_requests_allowed_to'])
        self.comment = json['comment']
        self.site_url = json['site_url']
        self.archive = safe(False, AttributeError, strtobool, json['archive'])
        self.date_archived_at = get_date(json['date_archived_at'])
        self.db_tags = json['db_tags']
        html = requests.get("https://rating.chgk.info/tournament/%s" % self.id).text
        dom = etree.HTML(html)
        for group in [
            [self.orgcommittee, 'Оргкомитет'],
            [self.authors, 'Редакторы'],
            [self.game_jury, 'Игровое жюри'],
            [self.jury_of_appeal, 'Апелляционное жюри']
        ]:
            links = dom.xpath('//div[@class="card"]/span[text()="%s"]/following-sibling::*/a[1]/@href' % group[1])
            group[0].clear()
            for link in links:
                idplayer = int(link.replace('https://rating.chgk.info/player/', ''))
                person, created = Person.objects.get_or_create(idplayer=idplayer)
                group[0].add(person)
                if created:
                    person.update()
        self.save()
        # print("tournament saved!")

    @staticmethod
    def update_list():
        page = 0
        while True:
            page += 1
            json = requests.get("https://rating.chgk.info/api/tournaments.json/?page=%s" % str(page)).json()
            if len(json['items']) > 0:
                for t in json['items']:
                    Tournament.objects.update_or_create(
                        idtournament=t['id'],
                        defaults={
                            'name': t['name'],
                            'date_start': get_date(t['date_start']),
                            'date_end': get_date(t['date_end']),
                            'type_name': str(t['type_name']),
                            'archive': False if t['archive'] is None else bool(int(t['archive'])),
                            'date_archived_at': get_date(t['date_archived_at'])
                        }
                    )
            else:
                break

    class Meta:
        verbose_name = "турнир"
        verbose_name_plural = "турниры"

    def link(self):
        return u'<a href="https://rating.chgk.info/tournament/%s">%s</a>' % (self.id, self.name)

    def __unicode__(self):
        return u'%s %s (%s)' % (self.id, self.name, self.type_name)

    def __str__(self):
        return self.__unicode__()


class Person(Model):
    id = PositiveIntegerField(unique=True, primary_key=True)
    json = TextField(null=True, blank=True, editable=False)
    surname = CharField(default="", max_length=30, editable=False)
    name = CharField(default="", max_length=30, editable=False)
    patronymic = CharField(default=None, null=True, max_length=30, editable=False)
    comment = TextField(default="", null=True, editable=False)
    db_chgk_info_tag = CharField(default=None, null=True, max_length=32, editable=False)

    town = CharField(default=None, null=True, max_length=30, editable=False)

    @staticmethod
    def update_list():
        page = 0
        while True:
            page += 1
            json = requests.get("https://rating.chgk.info/api/players.json/?page=%s" % str(page)).json()
            if len(json['items']) > 0:
                for t in json['items']:
                    Person.objects.update_or_create(
                        idplayer=t['id'],
                        defaults={
                            'surname': t['surname'],
                            'name': t['name'],
                            'patronymic': t['patronymic'],
                            'fio': ('%s %s %s' % (t['surname'], t['name'], t['patronymic'])).strip()
                        }
                    )
            else:
                break

    def update(self):
        json = get_by_id(self.id, "players")
        tournaments_json = get_by_id(self.id, "player_tournaments")
        saving = False

        if self.json != json:
            self.json = json
            self.surname = json['surname']
            self.name = json['name']
            self.patronymic = json['patronymic']
            self.comment = json['comment']
            self.db_chgk_info_tag = json['db_chgk_info_tag']
            self.fio = ('%s %s %s' % (json['surname'], json['name'], json['patronymic'])).strip()
            saving = True

        if saving:
            self.save()

    class Meta:
        verbose_name = "персона"
        verbose_name_plural = "персоны"

    def link(self):
        l = u'<a href="https://rating.chgk.info/player/%s">%s&nbsp;%s</a>'
        return l % (self.id, self.name, self.surname)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.id, self.surname, self.name, self.patronymic)

    def __str__(self):
        return self.__unicode__()


class Team(Model):
    id = PositiveIntegerField(unique=True, primary_key=True)
    json = TextField(default="", editable=False)
    name = CharField(default="", max_length=50, editable=False)
    town = CharField(default=None, null=True, max_length=30, editable=False)
    region_name = CharField(default=None, null=True, max_length=60, editable=False)
    country_name = CharField(default=None, null=True, max_length=90, editable=False)
    tournaments_this_season = PositiveSmallIntegerField(default=None, null=True, editable=False)
    tournaments_total = PositiveSmallIntegerField(default=None, null=True, editable=False)
    comment = TextField(default="", null=True, editable=False)

    @staticmethod
    def update_list():
        page = 0
        while True:
            page += 1
            json = requests.get("https://rating.chgk.info/api/teams.json/?page=%s" % page).json()
            if len(json['items']) > 0:
                for t in json['items']:
                    if t['town'] == 'Владивосток':
                        Team.objects.update_or_create(
                            idteam=t['id'],
                            defaults={
                                'name': t['name'],
                                'town': t['town'],
                                'region_name': t['region_name'],
                                'country_name': t['country_name'],
                                'tournaments_this_season': t['tournaments_this_season'],
                                'tournaments_total': t['tournaments_total']
                            }
                        )
            else:
                break

    def update(self):
        json = get_by_id(self.id, "teams")
        if self.json != json:
            self.json = json
            self.name = json['name']
            self.town = json['town']
            self.region_name = json['region_name']
            self.country_name = json['country_name']
            self.tournaments_this_season = json['tournaments_this_season']
            self.tournaments_total = json['tournaments_total']
            self.comment = json['comment']
            self.save()
            
    class Meta:
        verbose_name = "команда"
        verbose_name_plural = "команды"

    def __unicode__(self):
        return u'%s %s' % (self.id, self.name)

    def __str__(self):
        return self.__unicode__()
