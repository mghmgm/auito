from django.utils import timezone
from django.core.files import File
from django.core.management.base import BaseCommand
from app.models import User
from app.models import Post


class Command(BaseCommand):
    help = "Добавляет тестовую запись в модель Post"

    def handle(self, *args, **kwargs):
        user = User.objects.get(username="admin", is_staff=True, is_superuser=True)
        pub_date = timezone.now()

        # создаем тестовую запись
        with open("app/static/app/img/test_image.webp", "rb") as img_file:
            Post.objects.create(
                author=user,
                title="Тестовая запись",
                description="Это тестовое описание.",
                pub_date=pub_date,
                image=File(img_file),
            )

        self.stdout.write(self.style.SUCCESS("Добавлена тестовая запись!"))
