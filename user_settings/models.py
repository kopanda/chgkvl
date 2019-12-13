from django.db.models import *
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from rating.models import Person, Team
from accounting.models import Currency


class UserSettings(Model):
    user = OneToOneField(User, CASCADE, blank=True, null=True, verbose_name="пользователь")
    person = ForeignKey(Person, SET_NULL, blank=True, null=True, verbose_name="профиль на сайте рейтинга")
    default_currency = ForeignKey(Currency, SET_NULL, blank=True, null=True, verbose_name="валюта")
    town_id = PositiveSmallIntegerField(null=True, blank=True, verbose_name="город")
    email = EmailField(null=True, blank=True)
    phone = PhoneNumberField(blank=True)
    teams = ManyToManyField(Team, blank=True, verbose_name="команды игрока")

    class Meta:
        verbose_name = "настройки пользователя"
        verbose_name_plural = "настройки пользователей"

    def __unicode__(self):
        return '%s / %s' % (self.user, self.person)

    def __str__(self):
        return self.__unicode__()