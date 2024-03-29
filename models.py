import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from peewee import *

DATABASE = SqliteDatabase('social.db')

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField(max_length=100)
	joined_at = DateTimeField(default=datetime.datetime.now) # make sure not to have () for datetime.datetime.now
	is_admin = BooleanField(default=False)

	class Meta:
		database = DATABASE
		order_by = ('-joined_at', )

	# @classmethod - it will create the user model instance when it runs this methog and then use this
	@classmethod
	def create_user(cls, username, email, password, admin=False):
		try:
			cls.create(
				username=username,
				email=email,
				password=generate_password_hash(password),
				is_admin=admin
				)
		except IntegrityError:
			raise ValueError("User already exists")

def initialize():
    DATABASE.connect()
    DATABASE.create.tables([User]), safe=True)
    DATABASE.close()
