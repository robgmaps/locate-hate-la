from django.db import models
from django.utils import timezone 

# Create your models here.

# gnews api call
class APICall(models.Model):
	search_term = models.CharField(max_length=254, db_index=True)
	total_articles = models.IntegerField()
	dt_add = models.DateTimeField('date created', default=timezone.now)

	class Meta:
		ordering = [ '-dt_add', ]

	def __str__(self):
		return self.search_term

# returned article
class Article(models.Model):
	apicall = models.ForeignKey(APICall, on_delete=models.CASCADE)
	title = models.TextField()
	description = models.TextField()
	content = models.TextField()
	url = models.URLField(max_length=1000)
	image = models.URLField(max_length=1000)
	published_at = models.DateTimeField()
	source_name = models.TextField()
	source_url = models.URLField(max_length=1000)

	class Meta:
		ordering = [ '-published_at', ]

	def __str__(self):
		return self.title
