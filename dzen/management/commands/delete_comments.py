import sys

from django.core.management import BaseCommand

from dzen.models import Comment


class Command(BaseCommand):
    help = "Delete all comments"



    def handle(self, *args, **options):

        comments = Comment.objects.all()
        comments.delete()

        sys.stdout.write('Comments has been deleted \n')


