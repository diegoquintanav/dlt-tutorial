import argparse
import datetime as dt
import logging
from pathlib import Path
from typing import Generator

import dlt
from dlt.pipeline import TRefreshMode

# Create a logger
logger = logging.getLogger("dlt")

# Set the log level
logger.setLevel(logging.INFO)


# --8<-- [start:resource_decorator]
# --8<-- [start:resource]
@dlt.resource(
    name="sample_data",
    primary_key="id",
    write_disposition={"disposition": "merge", "strategy": "scd2"},
)
def sample_data(use_new_data: bool = False) -> Generator[dict, None, None]:
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

    # --8<-- [start:new_data]

    if use_new_data:
        print("Using new data for this run.")
        my_data = [
            {
                "id": 1,
                "name": "Jumpman",
                "uuid": "a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc",
                "created_at": "2025-10-09 14:40:00",
                "updated_at": "2025-10-10 11:50:00",
                "metadata": {
                    "ingested_at": dt.datetime.now().isoformat(),
                    "script_name": Path(__file__).name,
                },
            },
            {
                "id": 3,
                "name": "Ms. Peach",
                "uuid": "1a73f32f-9144-4318-9a00-4437bde41627",
                "created_at": "2025-10-12 13:15:00",
                "updated_at": "2025-10-13 13:50:00",
                "metadata": {
                    "ingested_at": dt.datetime.now().isoformat(),
                    "script_name": Path(__file__).name,
                },
            },
        ]
        # --8<-- [end:new_data]
    for item in my_data:
        yield item


# --8<-- [end:resource]


# --8<-- [start:source]
@dlt.source
def sample_source():
    yield sample_data


# --8<-- [end:source]


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
