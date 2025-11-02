import datetime as dt
from pathlib import Path
from typing import Generator

import dlt


# --8<-- [start:resource]
@dlt.resource(
    name="sample_data",
    write_disposition={
        "disposition": "replace",
    },
)
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


# --8<-- [end:resource]

if __name__ == "__main__":
    # --8<-- [start:pipeline]
    pipeline = dlt.pipeline(
        pipeline_name="sample_pipeline_postgres",
        destination=dlt.destinations.postgres,
        dataset_name="sample_data",
    )

    print("Starting pipeline...")
    load_info = pipeline.run(
        sample_data,
        table_name="samples",
        refresh="drop_sources",
    )
    # --8<-- [end:pipeline]
    print("Pipeline run completed.")
    # --8<-- [start:load_info]
    print(load_info)
    # --8<-- [end:load_info]
