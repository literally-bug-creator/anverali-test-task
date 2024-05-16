from sqlalchemy import Table, Column, Integer, String, MetaData


metadata_object = MetaData()

tasks_table = Table(
    "tasks",
    metadata_object,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("creator_id", String)
)