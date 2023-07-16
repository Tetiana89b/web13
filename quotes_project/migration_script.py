
import os
import sqlite3

import django
from django.db.models import Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_project.settings')
django.setup()


from datetime import datetime

from pymongo import MongoClient
from quotes_app.models import Author, Quote

# Підключення до MongoDB
client = MongoClient(
    'mongodb+srv://kara89:321321@cluster0.9wjid2s.mongodb.net/')
mongo_db = client['my_test']

# Підключення до SQLite
sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_cursor = sqlite_conn.cursor()

# Отримання даних з MongoDB
mongo_authors = mongo_db['author'].find()
mongo_quotes = mongo_db['quote'].find()

# Видалення дублікатів
duplicate_authors = Author.objects.values(
    'fullname').annotate(count=Count('id')).filter(count__gt=1)
for duplicate_author in duplicate_authors:
    author = Author.objects.filter(
        fullname=duplicate_author['fullname']).order_by('id').first()
    Author.objects.filter(fullname=duplicate_author['fullname']).exclude(
        id=author.id).delete()

# Збереження авторів у SQLite
for author in mongo_authors:
    fullname = author.get('fullname', '')
    born_date_str = author.get('born_date', '')
    born_date = datetime.strptime(born_date_str, "%B %d, %Y").strftime(
        "%Y-%m-%d") if born_date_str else None
    born_location = author.get('born_location', '')
    description = author.get('description', '')

    author_obj, created = Author.objects.get_or_create(
        fullname=fullname,
        defaults={'born_date': born_date,
                  'born_location': born_location, 'description': description}
    )
    if not created:
        author_obj.born_date = born_date
        author_obj.born_location = born_location
        author_obj.description = description
        author_obj.save()

# Збереження цитат у SQLite
for quote in mongo_quotes:
    author_id = str(quote['author'])
    try:
        author_obj = Author.objects.get(fullname=fullname)
        quote_obj = Quote(author=author_obj, quote=quote['quote'])
        quote_obj.save()
    except Author.DoesNotExist:
        print(
            f"Author with fullname '{fullname}' does not exist in the database.")

# Застосування змін до бази даних SQLite
sqlite_conn.commit()

# Закриття підключення до бази даних SQLite
sqlite_conn.close()

print("Data migration completed successfully.")
