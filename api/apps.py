import threading
import time
from datetime import timedelta

from django.apps import AppConfig
from django.utils import timezone

def start_token_cleaner():
    def cleaner():
        while True:
            from api.models import UserTokens
            cutoff = timezone.now() - timedelta(weeks=1)
            deleted_count, _ = UserTokens.objects.filter(time_of_creation__lt=cutoff).delete()
            if deleted_count:
                print(f'[TokenCleaner] Removed {deleted_count} tokens')
            time.sleep(3600)

    thread = threading.Thread(target=cleaner, daemon=True)
    thread.start()

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        import sys
        if 'runserver' in sys.argv:
            start_token_cleaner()
