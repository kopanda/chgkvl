# Generated by Django 2.2.7 on 2019-12-03 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('json', models.TextField(blank=True, editable=False, null=True)),
                ('surname', models.CharField(default='', editable=False, max_length=30)),
                ('name', models.CharField(default='', editable=False, max_length=30)),
                ('patronymic', models.CharField(default=None, editable=False, max_length=30, null=True)),
                ('comment', models.TextField(default='', editable=False, null=True)),
                ('db_chgk_info_tag', models.CharField(default=None, editable=False, max_length=32, null=True)),
                ('fio', models.CharField(default='', editable=False, max_length=92)),
                ('town', models.CharField(default=None, editable=False, max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'персона',
                'verbose_name_plural': 'персоны',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('json', models.TextField(default='', editable=False)),
                ('name', models.CharField(default='', editable=False, max_length=50)),
                ('town', models.CharField(default=None, editable=False, max_length=30, null=True)),
                ('region_name', models.CharField(default=None, editable=False, max_length=60, null=True)),
                ('country_name', models.CharField(default=None, editable=False, max_length=90, null=True)),
                ('tournaments_this_season', models.PositiveSmallIntegerField(default=None, editable=False, null=True)),
                ('tournaments_total', models.PositiveSmallIntegerField(default=None, editable=False, null=True)),
                ('comment', models.TextField(default='', editable=False, null=True)),
            ],
            options={
                'verbose_name': 'команда',
                'verbose_name_plural': 'команды',
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='', editable=False, max_length=100)),
                ('town', models.CharField(default=None, editable=False, max_length=30, null=True)),
                ('long_name', models.TextField(default='', editable=False, null=True)),
                ('date_start', models.DateTimeField(default=None, editable=False, null=True)),
                ('date_end', models.DateTimeField(default=None, editable=False, null=True)),
                ('tour_count', models.PositiveSmallIntegerField(default=None, editable=False, null=True)),
                ('tour_questions', models.PositiveSmallIntegerField(default=None, editable=False, null=True)),
                ('tour_ques_per_tour', models.CharField(default=None, editable=False, max_length=30, null=True)),
                ('questions_total', models.PositiveSmallIntegerField(default=None, editable=False, null=True)),
                ('type_name', models.CharField(default=None, editable=False, max_length=128, null=True)),
                ('main_payment_value', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=8)),
                ('main_payment_currency', models.CharField(default='', editable=False, max_length=10)),
                ('discounted_payment_value', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=8)),
                ('discounted_payment_currency', models.CharField(default='', editable=False, max_length=10, null=True)),
                ('discounted_payment_reason', models.TextField(default='', editable=False, null=True)),
                ('tournament_in_rating', models.BooleanField(default=False, editable=False)),
                ('date_requests_allowed_to', models.DateTimeField(editable=False, null=True)),
                ('comment', models.TextField(default='', editable=False, null=True)),
                ('site_url', models.CharField(default=None, editable=False, max_length=120, null=True)),
                ('archive', models.BooleanField(default=False, editable=False)),
                ('date_archived_at', models.CharField(default=None, editable=False, max_length=120, null=True)),
                ('db_tags', models.CharField(default=None, editable=False, max_length=120, null=True)),
                ('json', models.TextField(default='', editable=False)),
                ('authors', models.ManyToManyField(blank=True, related_name='authors', to='rating.Person', verbose_name='редакторы')),
                ('game_jury', models.ManyToManyField(blank=True, related_name='game_jury', to='rating.Person', verbose_name='игровое жюри')),
                ('jury_of_appeal', models.ManyToManyField(blank=True, related_name='jury_of_appeal', to='rating.Person', verbose_name='апелляционное жюри')),
                ('orgcommittee', models.ManyToManyField(blank=True, related_name='orgcommittee', to='rating.Person', verbose_name='организаторы')),
            ],
            options={
                'verbose_name': 'турнир',
                'verbose_name_plural': 'турниры',
            },
        ),
    ]
