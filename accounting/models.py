from django.db.models import *
from decimal import Decimal
import requests
from datetime import datetime
import xml.etree.ElementTree as Etree


class Currency(Model):
    code = CharField(default="", max_length=5, verbose_name="трёхсимвольный код")
    sign = CharField(default="", max_length=1, verbose_name="символ")
    name = CharField(default="", max_length=30, verbose_name="наименование")
    cbr_id = CharField(default="", max_length=30, verbose_name="ID Центробанка")
    rating_id = CharField(default="", max_length=5, verbose_name="обозначение на сайте рейтинга")

    def update(self):
        rates = Rate.objects.filter(currency=self).order_by("-date")
        first_date = rates[0].date.strftime("%d/%m/%Y") if len(rates) > 0 else '01/01/2019'
        if first_date != datetime.utcnow().date():
            second_date = datetime.utcnow().strftime("%d/%m/%Y")
            params = {'date_req1': first_date, 'date_req2': second_date, 'VAL_NM_RQ': self.cbr_id}
            xml = requests.get('http://www.cbr.ru/scripts/XML_dynamic.asp', params=params)
            root = Etree.fromstring(xml.text)
            for child in root.findall('Record'):
                Rate.objects.get_or_create(
                    currency=self,
                    date=datetime.strptime(child.attrib['Date'], "%d.%m.%Y"),
                    rate=Decimal(child[1].text.replace(",", "."))
                )

    class Meta:
        verbose_name = "валюта"
        verbose_name_plural = "валюты"

    def __unicode__(self):
        return u'%s' % self.sign

    def __str__(self):
        return self.__unicode__()


class Rate(Model):
    currency = ForeignKey(Currency, CASCADE, blank=True, null=True, verbose_name="валюта")
    date = DateField(verbose_name="дата")
    rate = DecimalField(max_digits=16, decimal_places=6, verbose_name="курс")

    class Meta:
        verbose_name = "курс валюты"
        verbose_name_plural = "курсы валют"

    def __unicode__(self):
        return u'%s — %s — %s' % (self.date, self.currency.code, self.rate)

    def __str__(self):
        return self.__unicode__()


class PaymentMethod(Model):
    name = CharField(max_length=120, blank=True, verbose_name="наименование")
    short_name = CharField(max_length=10, blank=True, verbose_name="краткое наименование")
    comment = TextField(blank=True, verbose_name="комментарий")

    class Meta:
        verbose_name = "способ оплаты"
        verbose_name_plural = "способы оплаты"

    def __unicode__(self):
        return u'%s' % self.short_name

    def __str__(self):
        return self.__unicode__()
