import json

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AssetRecord, Robot


@receiver(post_save, sender=Robot)
def init_asset_record(sender, instance: Robot, created=False, **kwargs):
    if created:
        AssetRecord.objects.create(
            currency=instance.target_currency, robot=instance,
        )


@receiver(post_save, sender=Robot)
def init_strategy_parameters(sender, instance: Robot, created=False, **kwargs):
    if created:
        param_spec = json.loads(instance.strategy_template.param_spec)
        parameters = {
            "version": param_spec["version"],
        }
        fields = {}
        for v in param_spec["fields"].values():
            fields[v["code"]] = v["default_value"]
        parameters["fields"] = fields
        instance.strategy_parameters = parameters
        instance.save(update_fields=["strategy_parameters"])
