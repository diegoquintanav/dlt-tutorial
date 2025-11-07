import argparse
import string
from typing import Generator
from uuid import uuid4

import dlt
from dlt.pipeline import TRefreshMode


@dlt.resource(
    primary_key="id",
)
def sample_data() -> Generator[dict, None, None]:
    for x in range(2):
        yield {
            "id": x,
            "name": "Mr. " + string.ascii_letters[x],
            "random_field": uuid4(),
        }


def transform_data(batch: list[dict]) -> Generator[dict, None, None]:
    for data in batch:
        data["my_transformed_field"] = (
            data["name"].lower().replace(".", "_").replace(" ", "_")
        )
        yield data


@dlt.source
def sample_source(my_custom_parameter: str = "foo"):
    print(f"Custom parameter value: {my_custom_parameter}")
    transformed_resource = transform_data(sample_data)
    yield transformed_resource


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
        pipeline_name="sample_pipeline",
        destination=dlt.destinations.postgres,
        dataset_name="sample_data",
    )

    refresh_mode: TRefreshMode = "drop_sources"
    load_info = pipeline.run(
        sample_source,
        table_name="samples",
        refresh=refresh_mode if should_refresh else None,
        write_disposition={
            "disposition": "replace",
        },
    )

    print(load_info)
