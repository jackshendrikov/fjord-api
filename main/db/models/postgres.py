from piccolo.columns import Text, Varchar
from piccolo.table import Table

from main.const.common import Language
from main.const.translator import Provider


class Translation(Table, help_text="Necessary info about translation"):  # type: ignore
    original = Text(help_text="Original Text", required=True)
    translated = Text(help_text="Translated Text", required=True)
    provider = Varchar(
        help_text="Translation Provider", choices=Provider, required=True
    )
    source = Varchar(
        help_text="Source Language of input text", choices=Language, required=True
    )
    target = Varchar(
        help_text="Target translation Language", choices=Language, required=True
    )
    text_hash = Varchar(
        help_text="Hash of original text", length=256, unique=True, required=True
    )
