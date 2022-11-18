import os

from piccolo.conf.apps import AppConfig

from main.apps.tables import Translation

CURRENT_DIRECTORY = os.path.dirname(__file__)


APP_CONFIG = AppConfig(
    app_name="translations",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "piccolo_migrations"),
    table_classes=[Translation],
    migration_dependencies=[],
    commands=[],
)
