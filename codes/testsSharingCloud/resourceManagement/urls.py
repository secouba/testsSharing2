from django.urls import include, path
from . import views # import views so we can use them in urls.

urlpatterns = [
    path('', views.index, name='index'),
    path('sign', views.signIn, name='sign'),
    path('base_user', views.base_user, name='user_home'),
    path('book', views.book, name='book'),
    path('book_lists', views.book_lists, name='lists'),
    path('book/<int:id_booking>/', views.edit_book, name='edit_book'),
    path('del/<int:id_booking>/', views.delete_book, name='delete_book'),
    path('signOut', views.index, name='signOut'),
]