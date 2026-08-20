from django.db import migrations, models


TURKISH_SOURCE_NAMES = [
    'Webrazzi', 'Log.com.tr', 'ShiftDelete.Net', 'DonanımHaber',
    'Webtekno', 'Chip Türkiye', 'NTV Teknoloji',
]


def set_languages(apps, schema_editor):
    Source = apps.get_model('news', 'Source')
    Source.objects.filter(name__in=TURKISH_SOURCE_NAMES).update(language='tr')


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_more_sources'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='language',
            field=models.CharField(
                choices=[('tr', 'Türkçe'), ('en', 'İngilizce')],
                default='en',
                max_length=2,
            ),
        ),
        migrations.RunPython(set_languages, reverse_noop),
    ]
