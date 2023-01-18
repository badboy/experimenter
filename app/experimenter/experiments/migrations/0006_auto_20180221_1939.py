# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-21 19:39
from __future__ import unicode_literals

from django.db import migrations, models


def update_dates(apps, schema_editor):  # pragma: no cover
    Experiment = apps.get_model("experiments", "Experiment")
    ExperimentChangeLog = apps.get_model("experiments", "ExperimentChangeLog")

    for experiment in Experiment.objects.all():
        try:
            start_date = ExperimentChangeLog.objects.get(
                experiment=experiment, old_status="Accepted", new_status="Launched"
            ).changed_on
            experiment.proposed_start_date = start_date
        except Exception:
            pass

        try:
            end_date = ExperimentChangeLog.objects.get(
                experiment=experiment, old_status="Launched", new_status="Complete"
            ).changed_on
            experiment.proposed_end_date = end_date
        except Exception:
            pass
        experiment.save()


def update_versions(apps, schema_editor):  # pragma: no cover
    Experiment = apps.get_model("experiments", "Experiment")

    for experiment in Experiment.objects.all():
        experiment.firefox_version = f"{experiment.firefox_version}.0"
        experiment.save()


def add_project_to_name(apps, schema_editor):  # pragma: no cover
    Experiment = apps.get_model("experiments", "Experiment")

    for experiment in Experiment.objects.all():
        experiment.name = f"{experiment.project.name} {experiment.name}"
        experiment.save()


class Migration(migrations.Migration):

    dependencies = [("experiments", "0005_experiment_short_description")]

    operations = [
        migrations.AddField(
            model_name="experiment",
            name="proposed_end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="experiment",
            name="proposed_start_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="experiment",
            name="firefox_version",
            field=models.CharField(
                choices=[
                    ("55.0", "55.0"),
                    ("56.0", "56.0"),
                    ("57.0", "57.0"),
                    ("58.0", "58.0"),
                    ("59.0", "59.0"),
                    ("60.0", "60.0"),
                    ("61.0", "61.0"),
                    ("62.0", "62.0"),
                    ("63.0", "63.0"),
                    ("64.0", "64.0"),
                ],
                max_length=255,
            ),
        ),
        migrations.RunPython(update_dates),
        migrations.RunPython(update_versions),
        migrations.RunPython(add_project_to_name),
    ]
