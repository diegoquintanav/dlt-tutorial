import argparse
import datetime as dt
from pathlib import Path
from typing import Generator

import dlt
from dlt.pipeline import TRefreshMode


@dlt.resource
def sample_data() -> Generator[dict, None, None]:
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


# --8<-- [start:new_data]
@dlt.resource
def new_data() -> Generator[dict, None, None]:
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
    for item in my_data:
        yield item


# --8<-- [end:new_data]
# --8<-- [start:source]
@dlt.source
def sample_source(my_custom_parameter: str = "foo", use_new_data: bool = False):
    print(f"Custom parameter value: {my_custom_parameter}")
    yield sample_data if not use_new_data else new_data


# --8<-- [end:source]


# --8<-- [start:parse_args]
def parse_args():
    parser = argparse.ArgumentParser(description="Sample DLT Pipeline with Append")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Refresh the data in the destination (if applicable)",
    )

    parser.add_argument(
        "--new-data",
        action="store_true",
        help="Assume new data is loaded this time",
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

    if args.new_data:
        print("Using new data for this run.")

    load_info = pipeline.run(
        sample_source(use_new_data=args.new_data),
        table_name="samples",
        refresh=refresh_mode if should_refresh else None,
        write_disposition={
            "disposition": "append",
        },
    )
    # --8<-- [end:parse_args]

    print(load_info)
    print("Done")
