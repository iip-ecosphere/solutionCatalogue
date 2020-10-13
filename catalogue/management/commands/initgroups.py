from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission, User

from catalogue import models

CATALOGUE_PERMS = {
    cls: ["add", "change", "delete", "view"]
    for cls in [
        models.ApplicationProfile,
        models.BaseData,
        models.BranchProven,
        models.BranchApplicable,
        models.Component,
        models.DataAnalysisProcess,
        models.Requirements,
        models.Source,
        models.Task,
        models.Use,
        models.TechnicalSpecification,
    ]
}
GROUPS_PERMISSIONS = {
    "Autoren": CATALOGUE_PERMS,
    "Moderatoren": {
        User: ["change", "delete", "view"],
        models.Profile: ["change", "delete", "view"],
        **CATALOGUE_PERMS,
    },
}


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Create default groups"

    def handle(self, *args, **options):
        print(CATALOGUE_PERMS)
        for group_name in GROUPS_PERMISSIONS:
            group, created = Group.objects.get_or_create(name=group_name)
            for model_cls in GROUPS_PERMISSIONS[group_name]:
                for perm_index, perm_name in enumerate(
                    GROUPS_PERMISSIONS[group_name][model_cls]
                ):
                    # Generate permission name as Django would generate it
                    codename = perm_name + "_" + model_cls._meta.model_name
                    try:
                        # Find permission object and add to group
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                        self.stdout.write(
                            "Adding " + codename + " to group " + group.__str__()
                        )
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")
