# Generated by Django 3.2 on 2022-04-29 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('active', models.BooleanField(default=True)),
                ('code', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='LateEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Late Entries',
            },
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, '1st year'), (2, '2nd year'), (3, '3rd year'), (4, '4th year')])),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('st_no', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Core.branch')),
                ('late_entry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Core.lateentry')),
                ('year', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Core.year')),
            ],
        ),
    ]
