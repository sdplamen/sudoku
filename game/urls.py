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

    # New validation endpoints
    path('validate/grid/', views.validate_grid_input, name='validate_grid'),
    path('validate/solution/<int:id>/', views.validate_solution_progress, name='validate_solution'),

    # API endpoints
    path('api/puzzles/', SudokuListCreateAPI.as_view(), name='api_puzzles'),
    path('api/puzzles/<int:pk>/solve/', SudokuSolveAPI.as_view(), name='api_solve'),
]