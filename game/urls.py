from django.urls import path
from game import views

urlpatterns = [
    path('', views.sudoku_view, name='sudoku_board'),
    path('new/', views.new_game, name='sudoku_new'),
]