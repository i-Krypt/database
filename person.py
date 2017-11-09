# from peewee import Model, CharField, SqliteDatabase, IntegerField, DecimalField
from peewee import *
from os import path
ROOT = path.dirname(path.realpath(__file__))
db = SqliteDatabase(path.join(ROOT, "users.db"))

class User(Model):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()
    class Meta:
        database = db
class Person(Model):
    owner = ForeignKeyField(User, related_name="persons")
    name = CharField()
    weight = DecimalField()
    age = IntegerField()
    class Meta:
        database = db



User.create_table(fail_silently=True)
Person.create_table(fail_silently=True)

#
# User.create(name="John Mark", email="john@yahoo.com",password="123456")
# User.create(name="Mary Jan", email="mjnet@yahoo.com",password="123456")
#
# Person.create(owner=1, name="paul", weight=34,age=10)
# Person.create(owner=1, name="Jennie", weight=60,age=17)

# user1 = User.get(id=1)
# print(user1.name)
# for x in user1.persons:
#     print(x.name)

# child = Person.get(id=1)
# print(child.owner.name, child.owner.email)

# pewee relationships 1 to many