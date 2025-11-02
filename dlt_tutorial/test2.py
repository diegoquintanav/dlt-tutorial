# Sample data containing pokemon details
import os
import dlt
from dlt.common.typing import TDataItems, TDataItem

data = [
    {"id": 1, "name": "bulbasaur", "size": {"weight": 6.9, "height": 0.7}},
    {"id": 4, "name": "charmander", "size": {"weight": 8.5, "height": 0.6}},
    {"id": 25, "name": "pikachu", "size": {"weight": 6, "height": 0.4}},
]


@dlt.resource(
    name="pokemon_resource",
    write_disposition={"disposition": "merge", "strategy": "upsert"},
    primary_key="id",
)
def pokemon() -> TDataItems:
    yield data


@dlt.source(name="pokemon_source")
def pokemon_source():
    yield pokemon


pipeline = dlt.pipeline(
    pipeline_name="pokemon_pipeline",
    destination=dlt.destinations.postgres,
    dataset_name="pokemon_data",
    # refresh="drop_sources",
)


USE_SOURCE = os.environ.get("USE_SOURCE", "0")
print(f"USE_SOURCE={USE_SOURCE}")
if USE_SOURCE == "1":
    # using source, it inserts duplicates
    print("Using source, may insert duplicates")
    load_info = pipeline.run(pokemon_source)
else:
    # using resource, does not insert duplicates
    print("Using resource, no duplicates")
    load_info = pipeline.run(pokemon)
print(load_info)
