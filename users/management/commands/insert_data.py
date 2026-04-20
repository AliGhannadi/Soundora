from django.core.management.base import BaseCommand
from faker import Faker
from users.models import User, Producer
from app.models import Music, Category
class Command(BaseCommand):
    help = "Inserts the fake data"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()
    def handle(self, *args, **options):
        for _ in range(5):
         user = User.objects.create_user(email=self.fake.email(), password="Test123456", username=self.fake.user_name())
         category = Category.objects.create(name=self.fake.sentence(nb_words=1))
         producer = Producer.objects.create(user=user, category=category, rating=3.3)
        for _ in range(10):
            category = Category.objects.create(name=self.fake.sentence(nb_words=1))
            music =  Music.objects.create(title=self.fake.sentence(nb_words=1), category=category, file="musics/Alan_Walker-Faded-musicDel-320/")
            music.producer.add(producer)
         
    