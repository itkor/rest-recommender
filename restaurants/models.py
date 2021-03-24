from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator

class Cuisine(models.Model):
	cuisine = models.CharField(max_length=50)

	def __str__(self):
		return self.cuisine


class Diet(models.Model):
	spec_diet = models.CharField(max_length=50)
	
	def __str__(self):
		return self.spec_diet


class Feature(models.Model):
	feature = models.CharField(max_length=50)
	
	def __str__(self):
		return self.feature


class Meal(models.Model):
	meal = models.CharField(max_length=50)
	
	def __str__(self):
		return self.meal


class Restaurant(models.Model):
	rest_id = models.CharField(max_length=200, unique = True, blank=True)
	rest_name = models.CharField(max_length=200, blank=True)
	rest_url = models.CharField(max_length=200, blank=True)
	rest_city = models.CharField(max_length=200, blank=True)
	rest_street = models.CharField(blank=True, max_length=200)
	map_url = models.CharField(max_length=200, blank=True)
	coordinates = models.CharField(max_length=200, blank=True)
	phone = models.CharField(blank=True, max_length=200)
	rest_info = models.TextField(blank=True)
	rest_rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MaxValueValidator(5.00)], blank=True)
	price = models.CharField(max_length=10, blank=True)
	rest_types = models.CharField(blank=True, max_length=200)
	order_online = models.BooleanField(default=False)
	safety_measures = models.BooleanField(default=False)
	cuisine = models.ManyToManyField('Cuisine', blank=True)
	spec_diet = models.ManyToManyField('Diet', blank=True)
	feature = models.ManyToManyField('Feature', blank=True)
	meals = models.ManyToManyField('Meal', blank=True)


	def __str__(self):
		return self.rest_name

	def get_absolute_url(self):
		return reverse('detail', kwargs={'restaurant_id': self.id})


class Rating(models.Model):
	five_stars = models.CharField(max_length=200)
	four_stars = models.CharField(max_length=200)
	three_stars = models.CharField(max_length=200)
	two_stars = models.CharField(max_length=200)
	one_stars = models.CharField(max_length=200)
	michelin_label = models.CharField(max_length=200)
	trav_choice_label = models.CharField(max_length=200)
	food_rating =  models.DecimalField(max_digits=3, decimal_places=2, validators=[MaxValueValidator(5.00)], blank=True)
	service_rating =  models.DecimalField(max_digits=3, decimal_places=2, validators=[MaxValueValidator(5.00)], blank=True)
	value_rating =  models.DecimalField(max_digits=3, decimal_places=2, validators=[MaxValueValidator(5.00)], blank=True)
	atmos_rating =  models.DecimalField(max_digits=3, decimal_places=2, validators=[MaxValueValidator(5.00)], blank=True)
	rest_total_reviews = models.IntegerField()
	rest_id = models.ForeignKey('Restaurant', models.CASCADE)

	def __str__(self):
		return (self.rest_id.rest_name)