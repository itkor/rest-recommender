from django.contrib import admin
from .models import Cuisine, Diet, Feature, Meal, Rating, Restaurant 

admin.site.register(Restaurant)
admin.site.register(Cuisine)
admin.site.register(Feature)
admin.site.register(Diet)
admin.site.register(Meal)
admin.site.register(Rating)



admin.site.site_header = "Restaurant Recommender Admin Site"
admin.site.site_title = "Recommender Admin site"
admin.site.index_title = "Recommender Admin site"
