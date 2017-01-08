import random
import string

from django.conf import settings
from django.db import models
from django_hosts.resolvers import reverse

from .validators import validate_url, validate_dot_com

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 5)
SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 10)


def code_generator(size=SHORTCODE_MIN, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


class ShortURLManager(models.Manager):
	def all(self, *args, **kwargs):
		qs_main = super().all(*args, **kwargs)
		qs = qs_main.filter(active=True)
		return qs


class ShortURL(models.Model):
	url = models.CharField(max_length=255, validators=[validate_url, validate_dot_com])
	shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
	updated_on = models.DateTimeField(auto_now=True)
	created_on = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	objects = ShortURLManager()

	def save(self, *args, **kwargs):
		if self.shortcode is None or self.shortcode == "":
			self.shortcode = self.create_shortcode(size=SHORTCODE_MIN)

		super().save(*args, **kwargs)

	def create_shortcode(self, size=SHORTCODE_MIN):
		new_code = code_generator(size=size)

		qs_exists = ShortURL.objects.filter(shortcode=new_code).exists()
		if qs_exists:
			return self.create_shortcode(size=size)

		return new_code

	def get_short_url(self):
		url_path = reverse("scode", kwargs={'shortcode': self.shortcode}, host='www', scheme='http')
		return url_path
