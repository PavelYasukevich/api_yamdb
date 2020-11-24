from django.apps import apps
from django.contrib import admin

config = apps.get_app_config('api')
for model in config.get_models():
    admin.site.register(model)
