from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from console.utils.scripts.subscriptions.stripemgt import cleanup_subs, refresh_subs

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--cancel_dangling', action='store_true', default=False)
        # return super().add_arguments(parser)
    def handle(self, *args: Any, **options: Any):
        cancel_dangling = options.get('cancel_dangling')
        print(cancel_dangling)
        refresh_subs()
        # cleanup_subs()