# Generated by Django 3.2.9 on 2021-11-09 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('given_name', models.CharField(max_length=255)),
                ('surname_at_birth', models.CharField(max_length=255)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
                'ordering': ['surname_at_birth'],
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_title', models.CharField(max_length=510)),
                ('created_in_DB', models.DateTimeField(auto_now_add=True)),
                ('source_type', models.CharField(choices=[('document (primary source)', 'document (primary source)'), ('document (secondary source)', 'document (secondary source)'), ('image (photograph / painting)', 'image (photograph / painting)'), ('other', 'other')], max_length=255)),
                ('source_file', models.FileField(upload_to=None)),
                ('source_creator', models.CharField(max_length=510)),
                ('source_date_of_creation', models.DateTimeField()),
                ('source_DOC_approximate', models.BooleanField()),
                ('source_description', models.TextField()),
                ('source_bibliographic_reference', models.TextField()),
                ('src_is_private', models.BooleanField()),
                ('created_in_DB_by_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('relationship_type', models.CharField(choices=[('parent of', 'parent of'), ('child of', 'child of'), ('spouse of', 'spouse of'), ('guardian of', 'guardian of'), ('ward of', 'ward of')], max_length=255)),
                ('relationship_is_private', models.BooleanField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('principle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='principle', to='private.person')),
                ('referent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='referent', to='private.person')),
                ('source', models.ManyToManyField(to='private.Source')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='sources',
            field=models.ManyToManyField(to='private.Source'),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_title', models.CharField(max_length=510)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('event_type', models.CharField(choices=[('birth', 'birth'), ('death', 'death'), ('baptism', 'baptism'), ('marriage', 'marriage'), ('divorce', 'divorce'), ('im-/em-migration', 'im-/em-migration'), ('other', 'other')], max_length=255)),
                ('event_description', models.TextField()),
                ('event_date', models.DateTimeField()),
                ('event_date_approximate', models.BooleanField()),
                ('place', models.CharField(max_length=510)),
                ('event_is_private', models.BooleanField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('event_people', models.ManyToManyField(to='private.Person')),
                ('sources', models.ManyToManyField(to='private.Source')),
            ],
        ),
        migrations.CreateModel(
            name='Epoch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('epoch_title', models.CharField(max_length=510)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('epoch_type', models.CharField(choices=[('residence', 'residence'), ('study / work', 'study / work'), ('other', 'other')], max_length=255)),
                ('epoch_description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('start_date_approximate', models.BooleanField()),
                ('end_date', models.DateTimeField()),
                ('end_date_approximate', models.BooleanField()),
                ('epoch_is_private', models.BooleanField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('epoch_people', models.ManyToManyField(to='private.Person')),
                ('sources', models.ManyToManyField(to='private.Source')),
            ],
        ),
        migrations.CreateModel(
            name='BiographicalInfoNugget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=510)),
                ('info', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('nugget_is_private', models.BooleanField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('people', models.ManyToManyField(to='private.Person')),
                ('sources', models.ManyToManyField(to='private.Source')),
            ],
        ),
        migrations.CreateModel(
            name='AlternativeName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('alternate_first', models.CharField(max_length=255)),
                ('alternate_surname', models.CharField(max_length=255)),
                ('alternative_type', models.CharField(choices=[('nickname, or non-legal a.k.a.', 'nickname, or non-legal a.k.a.'), ('legal change due to marriage', 'legal change due to marriage'), ('legal change due to immigration', 'legal change due to immigration'), ('other', 'other')], max_length=255)),
                ('explanation', models.TextField()),
                ('start_date_of_alternative', models.DateTimeField()),
                ('start_date_approximate', models.BooleanField()),
                ('end_date_of_alternative', models.DateTimeField()),
                ('end_date_approximate', models.BooleanField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('principle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='private.person')),
                ('sources', models.ManyToManyField(to='private.Source')),
            ],
        ),
    ]