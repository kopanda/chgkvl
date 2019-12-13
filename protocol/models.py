from django.db.models import *
from rating.models import Team, Person
from venue.models import Event


class Claim(Model):
    datetime = DateTimeField(auto_now=True)
    team = ForeignKey(Team, SET_NULL, blank=True, null=True, related_name="claims", verbose_name="команда на сайте рейтинга")
    name = CharField(blank=True, max_length=100, verbose_name="Название")
    event = ForeignKey(Event, SET_NULL, blank=True, null=True, related_name="claims", verbose_name="игра ЧГК")
    played = BooleanField(default=False, verbose_name="состав подан")

    def link(self):
        name = self.name if self.name else self.team.name
        if self.team:
            return '<a href="http://rating.chgk.info/team/%s">%s</a>' % (self.team.id, name)
        else:
            return name

    class Meta:
        verbose_name = "заявка"
        verbose_name_plural = "заявки"
        unique_together = ['team', 'event']

    def team_name(self):
        if self.name and self.team:
            return '%s (%s)' % (self.name, self.team)
        elif self.name and not self.team:
            return self.name
        elif not self.name and self.team:
            return self.team
        else:
            return None

    def __unicode__(self):
        if self.event and (self.team or self.name):
            return '%s — %s' % (self.event.tournament, self.team or self.name)
        else:
            return 'пустая заявка'

    def __str__(self):
        return self.__unicode__()


class Attendance(Model):
    ROLES = (
        ('К', 'Капитан'),
        ('Б', 'Базовый состав'),
        ('Л', 'Легионер'),
    )
    team = ForeignKey(Claim, SET_NULL, blank=True, null=True, related_name="attendances", verbose_name="команда")
    flag = CharField(max_length=1, null=True, blank=True, choices=ROLES, verbose_name="флаг")
    person = ForeignKey(Person, SET_NULL, blank=True, null=True, verbose_name="игрок")
    surname = CharField(default="", max_length=30)
    name = CharField(default="", max_length=30)
    patronymic = CharField(default=None, null=True, max_length=30)
    points = DecimalField(default=0, max_digits=8, decimal_places=2,  verbose_name="баллы")

    class Meta:
        verbose_name = "посещение"
        verbose_name_plural = "посещения"
