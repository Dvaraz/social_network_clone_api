from django.urls import path

# from search.views import Search
from search.views import SearchView, SearchUsersView


urlpatterns = [
    path('', SearchView.as_view(), name='search'),
    path('user/', SearchUsersView.as_view(), name='search_user'),
]
