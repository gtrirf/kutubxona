import random
from django.core.management.base import BaseCommand
from faker import Faker
from kitoblar.models import Book, Yozuvi, Tili, Author, Category

class Command(BaseCommand):
    help = 'Create random books for testing purposes'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of books to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        faker = Faker()

        categories = list(Category.objects.all())
        authors = list(Author.objects.all())
        writings = list(Yozuvi.objects.all())
        languages = list(Tili.objects.all())

        for _ in range(total):
            book = Book(
                title=faker.sentence(nb_words=4),
                yozuvi=random.choice(writings) if writings else None,
                tili=random.choice(languages) if languages else None,
                pages=random.randint(100, 1000),
                nashriyot=faker.company(),
                description=faker.text(),
                isbn=faker.isbn13(),
                author=random.choice(authors) if authors else None,
                realize_date=faker.date(),
                category=random.choice(categories) if categories else None,
                quantity=random.randint(1, 20),
            )
            book.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} books'))
