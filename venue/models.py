from django.db.models import *
import math
from datetime import datetime
from pytz import timezone
import plural_ru

from rating.models import Tournament
from accounting.models import Currency, Rate, PaymentMethod

tz = timezone('Asia/Vladivostok')
town_id = '60'


class Location(Model):
    name = CharField(max_length=120, verbose_name="наименование")
    short_name = CharField(max_length=30, verbose_name="краткое наименование")
    address = CharField(max_length=300, verbose_name="адрес")
    url = URLField(null=True, blank=True, verbose_name="ссылка")
    lon = DecimalField(null=True, blank=True, max_digits=9, decimal_places=6, verbose_name="широта")
    lat = DecimalField(null=True, blank=True, max_digits=9, decimal_places=6, verbose_name="долгота")

    class Meta:
        verbose_name = "место проведения"
        verbose_name_plural = "места проведения"

    def __unicode__(self):
        return '%s' % self.short_name

    def __str__(self):
        return self.__unicode__()


class Event(Model):
    datetime = DateTimeField(verbose_name="дата и время")
    location = ForeignKey(Location, SET_NULL, blank=True, null=True, verbose_name="место")
    tournament = ForeignKey(Tournament, SET_NULL, blank=True, null=True, verbose_name="турнир чгк")
    name = CharField(max_length=120, blank=True, verbose_name="наименование")
    description = TextField(blank=True, verbose_name="описание")
    difficulty = DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)

    # рассчитывается по составам команд
    teams_main = PositiveSmallIntegerField(blank=True, default=0, verbose_name="команд всего")
    teams_disc = PositiveSmallIntegerField(blank=True, default=0, verbose_name="команд со скидкой")
    teams_free = PositiveSmallIntegerField(blank=True, default=0, verbose_name="команд, играющих бесплатно")

    # берётся из карточки турнира
    fee_main = DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name="взнос")
    fee_main_rub = DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name="взнос в рублях")
    fee_disc = DecimalField(blank=True, null=True, max_digits=8, decimal_places=2, verbose_name="взнос со скидкой")
    fee_disc_rub = DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=2, verbose_name="взнос со скидкой в рублях")
    fee_comment = TextField(blank=True, null=True, verbose_name="комментарий к скидке")

    # оплата организаторам
    pay_before = DateField(null=True, blank=True, verbose_name="оплатить до")
    payment = DecimalField(blank=True, null=True, max_digits=8, decimal_places=2,  verbose_name="сумма оплаты")
    currency = ForeignKey(Currency, SET_NULL, blank=True, null=True, verbose_name="валюта")
    payment_rub = PositiveSmallIntegerField(blank=True, default=0, verbose_name="сумма оплаты в рублях")
    payment_method = ForeignKey(PaymentMethod, SET_NULL, blank=True, null=True, verbose_name="способ оплаты")
    payment_details = CharField(max_length=120, blank=True, verbose_name="реквизиты платежа")
    payment_day = DateField(null=True, blank=True, verbose_name="дата оплаты")
    notify_by = TextField(blank=True, verbose_name="уведомить об оплате")

    # плата с человека
    fee_player = DecimalField(
        blank=True, null=True, default=300, max_digits=8, decimal_places=2,  verbose_name="индивидуальный взнос")
    fee_points = DecimalField(
        blank=True, null=True, default=3, max_digits=8, decimal_places=2,  verbose_name="цена по абонементу")

    def update_from_rating(self):
        self.tournament.update()
        self.name = self.tournament.name
        self.fee_main = self.tournament.main_payment_value
        self.fee_disc = self.tournament.discounted_payment_value
        self.fee_comment = self.tournament.discounted_payment_reason
        self.currency = Currency.objects.get(rating_id=self.tournament.main_payment_currency)
        self.save()
        self.update_numbers()
        return True

    def update_numbers(self):
        self.currency.update()
        fee_date = min(self.datetime.date(), datetime.utcnow().date())
        pay_date = self.payment_day if self.payment_day else datetime.utcnow().date()
        fee_rate = Rate.objects.filter(currency=self.currency, date__lte=fee_date).order_by("-date")[0].rate
        pay_rate = Rate.objects.filter(currency=self.currency, date__lte=pay_date).order_by("-date")[0].rate
        self.payment = self.teams_main * self.fee_main + self.teams_disc * self.fee_disc
        self.payment_rub = math.ceil(self.payment * pay_rate)
        self.fee_main_rub = math.ceil(self.fee_main * fee_rate / 10) * 10
        self.fee_disc_rub = math.ceil(self.fee_disc * fee_rate / 10) * 10
        self.save()
        return True

    def fees_hint(self):
        x = '<table><tr><th>Категория</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th></tr>'
        for i in [['Основная', self.fee_main_rub], ['Льготная', self.fee_disc_rub]]:
            if i[1] is not None:
                x += '<tr><td>%s</td>' % i[0]
                for j in range(1, 7):
                    x += '<td>%s</td>' % round(i[1] / j)
                x += '</tr>'
        x += '</table>'
        return x

    class Meta:
        verbose_name = "игра ЧГК"
        verbose_name_plural = "игры ЧГК"

    def __unicode__(self):
        return '%s — %s — %s' % (
            self.datetime.astimezone(tz).strftime("%d.%m.%Y %H:%M"),
            self.location,
            self.name
        )

    def __str__(self):
        return self.__unicode__()
