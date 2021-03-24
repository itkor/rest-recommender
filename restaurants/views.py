from django.shortcuts import render, redirect
from django.views import View
from .models import Restaurant, Cuisine, Diet, Feature, Meal, Rating
from restaurants import recommender_engine
from .data import cities

def index(request):

	return render(request, 'index.html')

class Search(View):

	def get(self, request, *args, **kwargs):
		context = {
					'cuisines': Cuisine.objects.all(),
					'spec_diets': Diet.objects.all(),
					'features': Feature.objects.all(),
					'meals': Meal.objects.all(),
					'cities': cities.cities,
		}
		return render(request, 'search.html', context)
	
	def post(self, request, *args, **kwargs):
		return redirect(request, 'result.html')


class RestaurantResultView(View):
	def __init__(self):
		self.input_dict = {}
		self.location = ''
		self.Recommendation = recommender_engine.Recommendation

	def post(self, request, *args, **kwargs):
		context = {}
		"""
		Since multiple values were possible for some inputs, 
		request.POST.value() only got the last item,
		so I had use the lists() function to extract all inputs
		"""
		for i in request.POST.lists():
			if (i[0] == 'cuisines'):
				self.input_dict['cuisines'] = i[1]
			elif (i[0] == 'meals'):
				self.input_dict['meals'] = i[1]
			elif (i[0] == 'features'):
				self.input_dict['features'] = i[1]
			elif (i[0] == 'spec_diet'):
				self.input_dict['spec_diet'] = i[1]

		self.location = request.POST['location']
		
		def add_selected_input(name):
			if (name in request.POST.keys()):
				self.input_dict[name] = 1
		
		add_selected_input('michelin_label')
		add_selected_input('order_online')
		add_selected_input('safety_measures')

		rec = self.Recommendation(self.input_dict, self.location)
		result = rec.give_recommendation()
	# extract list of restaurant IDs from recommendations
		rest_id_list = []
		for i in result:
			rest_id_list.append(i['rest_id'])
		"""
		Using rest_id__in = rest_id_list changes the order 
		Therefore fetch all restaurants in the city the user entered,
		then sort the result of db query using recommendation order.
		"""
		city_rests = Restaurant.objects.filter(rest_city=self.location)
		sorted_result = []
		for i in rest_id_list:
			sorted_result.append(city_rests.get(rest_id=i))
		context['rec'] = sorted_result
		context['location'] = self.location
		return render(request, 'results.html', context)


class RestaurantDetailView(View):
	
	def get(self, request, *args, **kwargs):
		cuisines = []
		features = []
		restaurant = Restaurant.objects.get(id = kwargs['restaurant_id'])
		rating = Rating.objects.get(rest_id=restaurant)
		for item in restaurant.cuisine.values():
			cuisines.append(item['cuisine'])
		for item in restaurant.feature.values():
			features.append(item['feature'])
		context = {'restaurant': restaurant,
					'cuisines':cuisines,
					'features':features,
					'ratings': rating,
					}
		return render(request, 'detail.html', context)


def about(request):
	return render(request, 'about.html')

def contact(request):
	return render(request, 'contact.html')
