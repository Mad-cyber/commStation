from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
#callback fro the model system that is defined and using a signal https://docs.djangoproject.com/en/4.2/topics/signals/#:~:text=AppConfig)%3A%0A%20%20%20%20...-,def%20ready(self)%3A,-setting_changed.connect
    def ready(self):
        import accounts.signals
