from piccolo.columns import Text, Varchar
from piccolo.table import Table

from main.const.common import Language
from main.const.translator import Provider


class Translation(Table, help_text="Necessary info about translation"):  # type: ignore
    original = Text()
    translated = Text()
    provider = Varchar(choices=Provider)
    source = Varchar(choices=Language)
    target = Varchar(choices=Language)
    text_hash = Varchar(length=256)
