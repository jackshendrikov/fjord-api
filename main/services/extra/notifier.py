from collections import OrderedDict

from prettytable import PrettyTable
from requests import request

from main.core.config import get_app_settings
from main.core.logging import logger
from main.schemas.notifier import NotifierError

settings = get_app_settings()

# TODO: Add logging
# TODO: Add documentation


class NotificationService:
    """Service for send notification about unexpected translation error to TG group"""

    def send_notification(self, error: NotifierError) -> None:
        """
        Send notification to specific telegram group.

        :param error: notification error data.
        """
        message = self._generate_message(error=error)
        tg_msg = {"chat_id": settings.tg_chat_id, "text": message, "parse_mode": "HTML"}
        response = self._make_telegram_request(json=tg_msg)
        logger.info(
            f"Status of your message: {'Sent' if response['ok'] else 'Error during delivery'}"
        )

    def _generate_message(self, error: NotifierError) -> str:
        general_data = [
            ["SERVICE", "FJORD API"],
            ["ENVIRONMENT", settings.current_env.upper()],
        ]
        error_data = [["TASK ID", error.task_id], ["ERROR", error.error_msg]]

        message = OrderedDict(
            {
                "header": "🚨🚨🚨 ALERT 🚨🚨🚨",
                "general": self._generate_table(data=general_data),
                "query": f'<b>MONGO QUERY</b>: <code>{{"task_id": "{error.task_id}"}}</code>',
                "errors": self._generate_table(data=error_data),
            }
        )
        return "\n\n".join(message.values())

    @staticmethod
    def _generate_table(data: list[list[str]]) -> str:
        """
        Generate pretty table for specific data.

        :param data: list of list with 2 str params (column name + value)
        :return: markdown-like table.
        """
        table = PrettyTable(header=False, align="l", padding_width=2)
        table.add_rows(data)
        return f"<pre>{table}</pre>"

    @staticmethod
    def _make_telegram_request(json: dict) -> dict:
        """
        Make request to Telegram API endpoint.

        :param json: Dictionary of the necessary information to send with the request.
        :return: json response.
        """
        api_url = f"https://api.telegram.org/bot{settings.tg_bot_token}/sendMessage"

        response = request(method="POST", url=api_url, json=json)
        response.raise_for_status()

        logger.info("Successfully send notification to TG group!")
        return response.json()
