from django.apps import AppConfig


from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class StaffConfig(AppConfig):
    name = 'staff'
    icon = '<i class="material-icons">group</i>'
