import json

from django.core.management import call_command
from django.test import TestCase

from experimenter.experiments.models import NimbusExperiment, NimbusFeatureConfig
from experimenter.experiments.tests.factories import (
    NimbusFeatureConfigFactory,
    NimbusVersionedSchemaFactory,
)
from experimenter.features import Features
from experimenter.features.tests import (
    mock_invalid_remote_schema_features,
    mock_valid_features,
)


@mock_valid_features
class TestLoadFeatureConfigs(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Features.clear_cache()

    def test_loads_new_feature_configs(self):
        self.assertFalse(NimbusFeatureConfig.objects.filter(slug="someFeature").exists())
        call_command("load_feature_configs")

        feature_config = NimbusFeatureConfig.objects.get(slug="someFeature")
        schema = feature_config.schemas.get(version=None)

        self.assertEqual(feature_config.name, "someFeature")
        self.assertEqual(
            feature_config.description,
            "Some Firefox Feature",
        )
        self.assertEqual(
            json.loads(schema.schema),
            {
                "type": "object",
                "properties": {
                    "stringEnumProperty": {
                        "description": "String Property",
                        "type": "string",
                        "enum": ["v1", "v2"],
                    },
                    "boolProperty": {
                        "description": "Boolean Property",
                        "type": "boolean",
                    },
                    "intProperty": {
                        "description": "Integer Property",
                        "type": "integer",
                        "enum": [1, 2, 3],
                    },
                    "jsonProperty": {"description": "Arbitrary JSON Property"},
                },
                "additionalProperties": False,
            },
        )

        feature_config = NimbusFeatureConfig.objects.get(slug="prefSettingFeature")
        schema = feature_config.schemas.get(version=None)

        self.assertEqual(
            sorted(schema.sets_prefs),
            sorted(["nimbus.test.string", "nimbus.test.int", "nimbus.test.boolean"]),
        )

    def test_updates_existing_feature_configs(self):
        NimbusFeatureConfigFactory.create(
            name="someFeature",
            slug="someFeature",
            application=NimbusExperiment.Application.DESKTOP,
            schemas=[
                NimbusVersionedSchemaFactory.build(
                    version=None,
                    schema="{}",
                )
            ],
        )
        NimbusFeatureConfigFactory.create(
            name="prefSettingFeature",
            slug="prefSettingFeature",
            application=NimbusExperiment.Application.DESKTOP,
            schemas=[
                NimbusVersionedSchemaFactory.build(
                    version=None,
                    schema="{}",
                )
            ],
        )
        call_command("load_feature_configs")

        feature_config = NimbusFeatureConfig.objects.get(slug="someFeature")
        schema = feature_config.schemas.get(version=None)
        self.assertEqual(feature_config.name, "someFeature")
        self.assertEqual(
            feature_config.description,
            "Some Firefox Feature",
        )
        self.assertEqual(
            json.loads(schema.schema),
            {
                "type": "object",
                "properties": {
                    "stringEnumProperty": {
                        "description": "String Property",
                        "type": "string",
                        "enum": ["v1", "v2"],
                    },
                    "boolProperty": {
                        "description": "Boolean Property",
                        "type": "boolean",
                    },
                    "intProperty": {
                        "description": "Integer Property",
                        "type": "integer",
                        "enum": [1, 2, 3],
                    },
                    "jsonProperty": {"description": "Arbitrary JSON Property"},
                },
                "additionalProperties": False,
            },
        )

        feature_config = NimbusFeatureConfig.objects.get(slug="prefSettingFeature")

        self.assertEqual(
            sorted(feature_config.schemas.get(version=None).sets_prefs),
            sorted(["nimbus.test.string", "nimbus.test.int", "nimbus.test.boolean"]),
        )

    def test_handles_existing_features_with_same_slug_different_name(self):
        NimbusFeatureConfigFactory.create(
            name="Some Firefox Feature different name",
            slug="someFeature",
            application=NimbusExperiment.Application.DESKTOP,
            schemas=[
                NimbusVersionedSchemaFactory.build(
                    version=None,
                    schema="{}",
                )
            ],
        )
        call_command("load_feature_configs")

        feature_config = NimbusFeatureConfig.objects.get(slug="someFeature")
        self.assertEqual(feature_config.name, "someFeature")
        self.assertEqual(
            feature_config.description,
            "Some Firefox Feature",
        )

    def test_load_feature_set_features_slug_enabled_to_false_if_not_found_yaml(self):
        NimbusFeatureConfigFactory.create(
            slug="test-feature",
            application=NimbusExperiment.Application.DESKTOP,
            schemas=[
                NimbusVersionedSchemaFactory.build(
                    version=None,
                    schema="{}",
                )
            ],
            enabled=True,
        )

        call_command("load_feature_configs")

        feature_config = NimbusFeatureConfig.objects.get(slug="test-feature")
        self.assertFalse(feature_config.enabled)

    def test_load_feature_set_features_slug_enabled_to_false_with_duplicate_slug(self):
        feature_desktop = NimbusFeatureConfigFactory.create(
            slug="someFeature",
            application=NimbusExperiment.Application.DESKTOP,
            enabled=True,
            schemas=[
                NimbusVersionedSchemaFactory.build(
                    version=None,
                    schema="{}",
                )
            ],
        )

        feature_fenix = NimbusFeatureConfigFactory.create(
            slug="someFeature",
            application=NimbusExperiment.Application.FENIX,
            enabled=True,
            schemas=[
                NimbusVersionedSchemaFactory.build(
                    version=None,
                    schema="{}",
                )
            ],
        )

        call_command("load_feature_configs")

        feature_desktop = NimbusFeatureConfig.objects.get(
            slug="someFeature", application=NimbusExperiment.Application.DESKTOP
        )
        feature_fenix = NimbusFeatureConfig.objects.get(
            slug="someFeature", application=NimbusExperiment.Application.FENIX
        )
        self.assertTrue(feature_desktop.enabled)
        self.assertFalse(feature_fenix.enabled)


@mock_invalid_remote_schema_features
class TestLoadInvalidRemoteSchemaFeatureConfigs(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Features.clear_cache()

    def test_load_feature_config_ignores_invalid_remote_json(self):
        schema = "{}"
        NimbusFeatureConfigFactory.create(
            slug="cfr",
            application=NimbusExperiment.Application.DESKTOP,
            schemas=[
                NimbusVersionedSchemaFactory.build(
                    version=None,
                    schema=schema,
                ),
            ],
        )

        call_command("load_feature_configs")

        feature_config = NimbusFeatureConfig.objects.get(slug="cfr")
        self.assertEqual(feature_config.schemas.get(version=None).schema, schema)

    def test_load_feature_does_not_set_no_features_slug_enabled_to_false(self):

        call_command("load_feature_configs")

        feature_config = NimbusFeatureConfig.objects.get(slug="no-feature-fenix")
        self.assertEqual(feature_config.enabled, True)
