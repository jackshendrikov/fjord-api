import uuid


def gen_export_sheet_url(spreadsheet_id: str, sheet_id: int) -> str:
    """
    Generate valid export Goggle Sheet link for CSV format.
    """

    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?gid={sheet_id}&format=csv"


def generate_task_id() -> str:
    """Return unique string for task id."""

    return uuid.uuid4().hex


def form_error_message(errors: list[dict]) -> list[str]:
    """
    Make valid pydantic `ValidationError` messages list.
    """

    messages = []
    for error in errors:
        field, message = error["loc"][-1], error["msg"]
        messages.append(f"`{field}` {message}")
    return messages
