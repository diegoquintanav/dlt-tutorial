import string
from typing import Generator
from uuid import uuid4

import dlt


@dlt.resource
def sample_data() -> Generator[dict, None, None]:
    for x in range(2):
        yield {
            "id": x,
            "name": "Mr. " + string.ascii_letters[x],
            "random_field": uuid4(),
        }


@dlt.source
def sample_source():
    yield sample_data


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="sample_pipeline",
        destination=dlt.destinations.duckdb,
        dataset_name="sample_data",
    )

    load_info = pipeline.run(
        sample_source,
        table_name="samples",
        write_disposition={
            "disposition": "replace",
        },
    )

    print(load_info)
