import datetime as dt
import random
import string
from typing import Generator
from uuid import uuid4

import dlt


def sample_data() -> Generator[dict, None, None]:
    yield [
        {
            "id": 1,
            "name": "Mr. Mario",
            "random_field": "a6d7b6dd-bcdb-422e-83eb-f53b2eb4f2cc",
            "created_at": "2025-10-09 14:40:00",
            "updated_at": "2025-10-09 14:50:00",
        },
        {
            "id": 2,
            "name": "Mr. Luigi",
            "random_field": "8c804ede-f8ae-409e-964d-9e355a3094e0",
            "created_at": "2025-10-08 16:15:00",
            "updated_at": "2025-10-08 16:50:00",
        },
    ]


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="sample_pipeline",
        destination=dlt.destinations.duckdb,
        dataset_name="sample_data",
    )

    print("Running pipeline...")

    load_info = pipeline.run(
        sample_data,
        table_name="samples",
        refresh="drop_sources",
        write_disposition={
            "disposition": "replace",
        },
    )

    print("Done")
    print("Load info:")
    print(load_info)
