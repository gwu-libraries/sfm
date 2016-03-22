import json
from .rabbit import RabbitWorker
from .models import SeedSet, Harvest
from django.core.exceptions import ObjectDoesNotExist
import logging
import datetime
from django.conf import settings
from django.db import transaction

log = logging.getLogger(__name__)


@transaction.atomic
def seedset_harvest(seedset_id):

    message = {
        "collection": {},
        "seeds": []
    }

    # Retrieve seedset
    try:
        seed_set = SeedSet.objects.get(id=seedset_id)
    except ObjectDoesNotExist:
        log.error("Harvesting seedset %s failed because seedset does not exist", seedset_id)
        return
    if not seed_set.is_active:
        log.debug("Ignoring Harvest for seedset as seedset %s is inactive", seedset_id)
        return

    historical_seed_set = seed_set.history.all()[0]
    historical_credential = historical_seed_set.credential.history.all()[0]
    historical_seeds = []
    for seed in seed_set.seeds.all():
        if seed.is_active:
            historical_seeds.append(seed.history.all()[0])
    if not historical_seeds:
        log.warning("Seedset %s has no seeds", seedset_id)
        return

    # Id
    harvest_id = "harvest:{}:{}".format(seedset_id, datetime.datetime.now().isoformat())
    message["id"] = harvest_id

    # Collection
    collection = historical_seed_set.collection
    message["collection"]["id"] = "collection:{}".format(collection.id)
    message["collection"]["path"] = "{}/collection/{}".format(settings.SFM_DATA_DIR, collection.id)

    # Credential
    message["credentials"] = json.loads(str(historical_credential.token))

    # Type
    harvest_type = historical_seed_set.harvest_type
    message["type"] = harvest_type

    # Options
    message["options"] = json.loads(historical_seed_set.harvest_options or "{}")

    # Seeds
    for historical_seed in historical_seeds:
        if historical_seed.is_active:
            seed_map = {}
            if historical_seed.token:
                seed_map["token"] = historical_seed.token
            if historical_seed.uid:
                seed_map["uid"] = historical_seed.uid
            message["seeds"].append(seed_map)

    routing_key = "harvest.start.{}.{}".format(historical_credential.platform, harvest_type)

    log.debug("Sending %s message to %s with id %s", harvest_type, routing_key, harvest_id)

    # Publish message to queue via rabbit worker
    RabbitWorker().send_message(message, routing_key)

    # Record harvest model instance
    harvest = Harvest.objects.create(harvest_id=harvest_id,
                                     historical_seed_set=historical_seed_set,
                                     historical_credential=historical_credential)
    harvest.historical_seeds.add(*historical_seeds)
