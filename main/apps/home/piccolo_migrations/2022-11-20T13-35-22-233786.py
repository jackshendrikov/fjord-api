from enum import Enum

from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text, Varchar
from piccolo.columns.indexes import IndexMethod

ID = "2022-11-20T13:35:22:233786"
VERSION = "0.96.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="translations", description=DESCRIPTION
    )

    manager.add_table("Translation", tablename="translation")

    manager.add_column(
        table_class_name="Translation",
        tablename="translation",
        column_name="original",
        db_column_name="original",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="Translation",
        tablename="translation",
        column_name="translated",
        db_column_name="translated",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="Translation",
        tablename="translation",
        column_name="provider",
        db_column_name="provider",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "Provider",
                {
                    "GOOGLE_TRANSLATE": "Google Translate",
                    "DEEPL": "Deepl",
                    "LIBRE_TRANSLATE": "LibreTranslate",
                    "MYMEMORY": "MyMemory",
                },
            ),
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="Translation",
        tablename="translation",
        column_name="source",
        db_column_name="source",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "Language",
                {
                    "AUTO": "autodetect",
                    "EN": "en",
                    "JP": "ja",
                    "IT": "it",
                    "GE": "de",
                    "UA": "uk",
                },
            ),
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="Translation",
        tablename="translation",
        column_name="target",
        db_column_name="target",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "Language",
                {
                    "AUTO": "autodetect",
                    "EN": "en",
                    "JP": "ja",
                    "IT": "it",
                    "GE": "de",
                    "UA": "uk",
                },
            ),
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="Translation",
        tablename="translation",
        column_name="text_hash",
        db_column_name="text_hash",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 256,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": True,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    return manager
