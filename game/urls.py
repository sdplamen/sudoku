from django.urls import path
from . import views
from .views import SudokuListCreateAPI, SudokuSolveAPI

urlpatterns = [
    path('', views.start, name='start'),
    path('new/', views.new, name='new'),
    path('solve/<int:id>/', views.to_solve, name='to_solve'),
    path('solved/<int:id>/', views.solved, name='solved'),
    path('check/<int:id>/', views.check_solution, name='check_solution'),
    path('clear/', views.clear_grids, name='clear_grids'),
    path('api/puzzles/', SudokuListCreateAPI.as_view(), name='api_puzzles'),
    path('api/puzzles/<int:pk>/solve/', SudokuSolveAPI.as_view(), name='api_solve'),
]