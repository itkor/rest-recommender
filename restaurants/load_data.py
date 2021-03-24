"""
Migrate restaurants from mongodb stored as a pickle file (pandas df) to SQLite
Using python manage.py shell - loop through each restaurant in the rests_info_df.pickle file 
and use functions below to add it to Restaurant, Cuisine, Diet, and Meal models.
"""

rest = None

# Create a Restaurant object with main information
def add_rest(i)

	rest = Restaurant.objects.create(
		rest_id = restaurants.iloc[i]['rest_id'], 
		rest_name = restaurants.iloc[i]['rest_name'],
		rest_url = restaurants.iloc[i]['rest_url'],
		rest_city = restaurants.iloc[i]['rest_city'],
		rest_street = restaurants.iloc[i]['rest_street'],
		rest_rating = restaurants.iloc[i]['rest_rating'],
		rest_info = restaurants.iloc[i]['about'],
		price = restaurants.iloc[i]['price_range_delta'],
		map_url = restaurants.iloc[i]['map_url'],
		coordinates = restaurants.iloc[i]['coordinates'],
		phone = restaurants.iloc[i]['phone'],
		rest_types = restaurants.iloc[i]['rest_types'],
		# order_online & safety_measures are either 0 (false) or 1 (true)
		order_online = (lambda x: x == 1)(restaurants.iloc[i]['order_online']),
		safety_measures = (lambda x: x == 1)(restaurants.iloc[i]['safety_measures'])
		)

# Using the rest object above, create a rating then add it with the restaurant as a FK
def add_rating(i)
	rating = Rating.objects.create(
		rest_id = rest, 
		five_stars = restaurants.iloc[i]['review_5_count'],
		four_stars = restaurants.iloc[i]['review_4_count'],
		three_stars = restaurants.iloc[i]['review_3_count'],
		two_stars = restaurants.iloc[i]['review_2_count'],
		one_stars = restaurants.iloc[i]['review_1_count'],
		michelin_label = restaurants.iloc[i]['michelin_label'],
		trav_choice_label = restaurants.iloc[i]['trav_choice_label'],
		food_rating = restaurants.iloc[i]['food_rating'],
		service_rating = restaurants.iloc[i]['service_rating'],
		value_rating = restaurants.iloc[i]['value_rating'],
		atmos_rating = restaurants.iloc[i]['atmos_rating'],
		rest_total_reviews = restaurants.iloc[i]['rest_total_reviews']
		)

# For each feature, cuisine, special diet, and meal found, check if it already exists, 
# otherwise create a new record then add a relationship to the restaurant.
def add_feature(c):
	features = restaurants.iloc[c]['features']
	if isinstance(features, str):
			features = features.split(',')
			for feature in features:
					try:
							f = Feature.objects.get(feature=feature)
					except:
							f = Feature.objects.create(feature=feature)
						rest.feature.add(f)

def add_cuisines(c):
	cuisines = restaurants.iloc[c]['cuisines']
	if isinstance(cuisines, str):
			cuisines = cuisines.split(',')
			for i in cuisines:
					try:
							f = Cuisine.objects.get(cuisine=i)
					except:
							f = Cuisine.objects.create(cuisine=i)
					rest.cuisine.add(f)

def add_spec_diet(c):
	spec_diet = restaurants.iloc[c]['spec_diet']
	if isinstance(spec_diet, str):
			spec_diet = spec_diet.split(',')
			for i in spec_diet:
					try:
							f = Diet.objects.get(spec_diet=i)
					except:
							f = Diet.objects.create(spec_diet=i)
					rest.spec_diet.add(f)



def add_meals(c):
	meals = restaurants.iloc[c]['meals']
	if isinstance(meals, str):
			meals = meals.split(',')
			for i in meals:
					try:
							f = Meal.objects.get(meal=i)
					except:
							f = Meal.objects.create(meal=i)
					rest.meals.add(f)