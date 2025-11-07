import argparse
import datetime as dt
import string
from typing import Generator
from uuid import UUID, uuid4

import dlt
from dlt.pipeline import TRefreshMode
from dlt.common.typing import TDataItems
from pydantic import BaseModel
from pathlib import Path


# --8<-- [start:pydantic_models]
class SampleDataMetadataModel(BaseModel):
    ingested_at: dt.datetime
    script_name: str


class SampleDataModel(BaseModel):
    id: int
    name: str
    uuid: UUID
    created_at: dt.datetime
    updated_at: dt.datetime
    metadata: SampleDataMetadataModel


# --8<-- [end:pydantic_models]


# --8<-- [start:resource_decorator]
# --8<-- [start:resource]
# --8<-- [start:columns_and_hints]
@dlt.resource(
    name="sample_data",
    primary_key="id",
    write_disposition="replace",
    columns=SampleDataModel,
    # --8<-- [end:columns_and_hints]
    schema_contract={
        "tables": "evolve",
        "columns": "freeze",
        "data_type": "freeze",
    },
)
def sample_data() -> TDataItems:
    # --8<-- [end:resource_decorator]
    my_data = [
        {
            "id": 1,
            "name": "Mr. Mario",
            "uuid": "a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc",
            "created_at": "2025-10-09 14:40:00",
            "updated_at": "2025-10-09 14:50:00",
            "metadata": {
                "ingested_at": dt.datetime.now().isoformat(),
                "script_name": Path(__file__).name,
            },
        },
        {
            "id": 2,
            "name": "Mr. Luigi",
            "uuid": "8c804ede-f8ae-409e-964d-9e355a3094e0",
            "created_at": "2025-10-08 16:15:00",
            "updated_at": "2025-10-08 16:50:00",
            "metadata": {
                "ingested_at": dt.datetime.now().isoformat(),
                "script_name": Path(__file__).name,
            },
        },
    ]

    for item in my_data:
        yield item


# --8<-- [end:resource]


# --8<-- [start:parse_args]
def parse_args():
    parser = argparse.ArgumentParser(description="Sample DLT Pipeline with Append")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Refresh the data in the destination (if applicable)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    should_refresh = args.refresh
    pipeline = dlt.pipeline(
        pipeline_name="sample_pipeline_postgres",
        destination=dlt.destinations.postgres,
        dataset_name="sample_data",
    )
    print("Running pipeline...")
    refresh_mode: TRefreshMode = "drop_sources"

    if should_refresh:
        print("Refreshing data in the destination.")

    # --8<-- [start:pipeline_run]
    load_info = pipeline.run(
        sample_data,
        refresh=refresh_mode if should_refresh else None,
        table_name="samples",
    )
    # --8<-- [end:pipeline_run]
    # --8<-- [end:parse_args]

    print(load_info)
    print("Done")
