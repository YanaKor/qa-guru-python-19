from pathlib import Path


def load_schema(schema):
    return str(Path(__file__).parent.parent.joinpath(f"schemas/{schema}"))
