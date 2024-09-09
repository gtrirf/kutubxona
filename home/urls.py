from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='home'),
    path('blog/create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('blog/<int:pk>/detail/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('search-results/', views.SearchResultsView.as_view(), name='search-results')
]