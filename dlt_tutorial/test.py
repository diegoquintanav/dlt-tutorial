import argparse
import datetime as dt
import logging
from pathlib import Path
from typing import Generator

import dlt
from dlt.pipeline import TRefreshMode


@dlt.resource(
    name="samples",
    primary_key="id",
    write_disposition="merge",
)
def samples() -> Generator[dict, None, None]:
    my_data = [
        {
            "id": 1,
            "name": "Mr. Mario",
            "uuid": "a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc",
            "created_at": "2025-10-09 14:40:00",
            "updated_at": "2025-10-09 14:50:00",
        },
        {
            "id": 2,
            "name": "Mr. Luigi",
            "uuid": "8c804ede-f8ae-409e-964d-9e355a3094e0",
            "created_at": "2025-10-08 16:15:00",
            "updated_at": "2025-10-08 16:50:00",
        },
    ]

    for item in my_data:
        yield item


@dlt.source(name="sample_source")
def sample_source():
    yield samples


if __name__ == "__main__":
    import os

    refresh = os.environ.get("REFRESH", "0")

    pipeline = dlt.pipeline(
        pipeline_name="sample_pipeline_postgres",
        destination=dlt.destinations.postgres,
        refresh="drop_sources" if refresh == "1" else None,
        dataset_name="sample_data",
    )

    load_info = pipeline.run(
        sample_source,
    )
