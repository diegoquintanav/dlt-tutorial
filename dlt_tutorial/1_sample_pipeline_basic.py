import datetime as dt
from pathlib import Path
from typing import Generator

import dlt


# --8<-- [start:sample_data]
def sample_data() -> Generator[dict, None, None]:
    data = [
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
    for item in data:
        yield item


# --8<-- [end:sample_data]

if __name__ == "__main__":
    # --8<-- [start:pipeline]
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

    # --8<-- [end:pipeline]
    print("Done")
    # --8<-- [start:load_info]
    print("Load info:")
    print(load_info)
    # --8<-- [end:load_info]
