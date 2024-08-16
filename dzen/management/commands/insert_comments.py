import sys

from django.core.management import BaseCommand
from faker import Faker

from dzen.models import Comment


class Command(BaseCommand):
    help = "Insert 10 new comments to the system"

    def add_arguments(self, parser):
        parser.add_argument("-l", "--len", type=int, default=10)

    def handle(self, *args, **options):
        faker = Faker()
        sys.stdout.write("Start inserting Comments \n")

        for _ in range(options["len"]):
            comment = Comment()
            comment.username = faker.user_name()
            comment.email = faker.email()
            comment.home_page = faker.url()
            comment.message = faker.text()
            comment.save()

        sys.stdout.write("End inserting Comments \n")
