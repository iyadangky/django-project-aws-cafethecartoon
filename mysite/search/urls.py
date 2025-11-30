from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
path('', views.gotomain, name="gotomain"),
path('search/', views.search, name='search'),
path('orderby/', views.orderby, name="orderby"),
path('insert/', views.insert, name="insert"),
path('new/', views.new, name="new"),
path('export_list/', views.export_list, name="export_list"),
path('export_content/', views.export_content, name="export_content"),
path('<int:book_id>/', views.edit, name="edit"),
path('<int:book_id>/update/', views.update, name="update"),
path('<int:book_id>/delete/', views.delete, name="delete"),

]
