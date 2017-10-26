from haystack import indexes
from .models import Movie

class MovieIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	name = indexes.CharField(model_attr='name')
	nation = indexes.CharField(model_attr='nation')
	category = indexes.CharField(model_attr='category')
	star = indexes.CharField(model_attr='star')

	def get_model(self):
		return Movie

	def index_queryset(self, using=None):
		return self.get_model().objects.all()