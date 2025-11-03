import argparse
import datetime as dt
import logging
from pathlib import Path

import dlt
from dlt.pipeline import TRefreshMode
from dlt.common.typing import TDataItems

# Create a logger
logger = logging.getLogger("dlt")

# Set the log level
logger.setLevel(logging.INFO)


# --8<-- [start:resource_decorator]
# --8<-- [start:resource]
# --8<-- [start:columns_and_hints]
@dlt.resource(
    name="sample_data",
    primary_key="id",
    write_disposition="replace",
    columns={
        "id": {"data_type": "bigint"},
        "name": {"data_type": "text"},
        "uuid": {"data_type": "text"},
        "created_at": {"data_type": "timestamp"},
        "updated_at": {"data_type": "timestamp"},
    },
    nested_hints={
        "metadata": dlt.mark.make_nested_hints(
            columns=[
                {
                    "name": "ingested_at",
                    "data_type": "timestamp",
                },
                {
                    "name": "script_name",
                    "data_type": "text",
                },
            ]
        ),
    },
    # --8<-- [end:columns_and_hints]
    schema_contract={
        "tables": "evolve",
        "columns": "freeze",
        "data_type": "evolve",
    },
)
def sample_data() -> TDataItems:
    # --8<-- [end:resource_decorator]
    # --8<-- [start:my_data]
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
    # --8<-- [end:my_data]

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
