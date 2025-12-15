from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = "Create admin user"

    def handle(self, *args, **kwargs):
        admin, created = User.objects.get_or_create(
            email="admin@gmail.com",
            defaults={"is_admin": True}
        )

        admin.set_password("admin123")
        admin.is_admin = True
        admin.save()

        self.stdout.write(self.style.SUCCESS(
            "ADMIN CREATED SUCCESSFULLY"
        ))
