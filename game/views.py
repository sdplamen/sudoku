import json

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Grid
from .forms import SudokuForm, LevelForm
from .sudoku import solve, is_valid_input
from random import choice


@require_http_methods(["POST"])
def validate_grid_input(request): 
    try: 
        data = json.loads(request.body)
        grid_data = data.get('grid_data', {})

        grid_dict = {}
        rows = 'ABCDEFGHI'
        cols = '123456789'

        for r in rows: 
            for c in cols: 
                key = f"{r}{c}"
                value = grid_data.get(key, '.')
                grid_dict[key] = value if value else '.'

        duplicates = []
        filled_count = 0

        for row in rows: 
            seen = {}
            for col in cols: 
                key = f"{row}{col}"
                value = grid_dict[key]
                if value != '.': 
                    filled_count += 1
                    if value in seen: 
                        duplicates.append(key)
                        duplicates.append(seen[value])
                    else: 
                        seen[value] = key

        for col in cols: 
            seen = {}
            for row in rows: 
                key = f"{row}{col}"
                value = grid_dict[key]
                if value != '.': 
                    if value in seen: 
                        if key not in duplicates: 
                            duplicates.append(key)
                        if seen[value] not in duplicates: 
                            duplicates.append(seen[value])
                    else: 
                        seen[value] = key

        block_rows = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
        block_cols = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

        for block_row in block_rows: 
            for block_col in block_cols: 
                seen = {}
                for row in block_row: 
                    for col in block_col: 
                        key = f"{row}{col}"
                        value = grid_dict[key]
                        if value != '.': 
                            if value in seen: 
                                if key not in duplicates: 
                                    duplicates.append(key)
                                if seen[value] not in duplicates: 
                                    duplicates.append(seen[value])
                            else: 
                                seen[value] = key

        duplicates = list(set(duplicates))

        is_valid = len(duplicates) == 0
        has_minimum = filled_count >= 17

        return JsonResponse({
            'is_valid': is_valid,
            'duplicates': duplicates,
            'filled_count': filled_count,
            'has_minimum': has_minimum,
            'message': get_validation_message(is_valid, filled_count, len(duplicates))
        })

    except Exception as e: 
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["POST"])
def validate_solution_progress(request, id): 
    try: 
        grid_obj = get_object_or_404(Grid, pk=id)
        solution = solve(grid_obj.grid)

        if not solution: 
            return JsonResponse({'error': 'Cannot solve puzzle'}, status=400)

        data = json.loads(request.body)
        user_input = data.get('user_input', {})

        initial_cells = []
        rows, cols = "ABCDEFGHI", "123456789"
        for i, char in enumerate(grid_obj.grid): 
            if char != '.': 
                field_name = f"{rows[i // 9]}{cols[i % 9]}"
                initial_cells.append(field_name)

        wrong_cells = []
        correct_cells = []
        filled_count = 0

        for key in solution.keys(): 
            user_val = user_input.get(key, '')

            if user_val: 
                filled_count += 1
                # Only validate user-entered cells (not initial cells)
                if key not in initial_cells: 
                    if user_val != solution[key]: 
                        wrong_cells.append(key)
                    else: 
                        correct_cells.append(key)

        is_complete = filled_count == 81 and len(wrong_cells) == 0

        return JsonResponse({
            'wrong_cells': wrong_cells,
            'correct_cells': correct_cells,
            'initial_cells': initial_cells,
            'filled_count': filled_count,
            'is_complete': is_complete,
            'message': get_progress_message(len(wrong_cells), is_complete)
        })

    except Exception as e: 
        return JsonResponse({'error': str(e)}, status=400)


def get_validation_message(is_valid, filled_count, duplicate_count): 
    if duplicate_count > 0: 
        return f'⚠️ {duplicate_count} duplicate(s) found! Fix them to continue.'
    elif is_valid and filled_count >= 17: 
        return '✓ Grid is valid! Ready to create puzzle.'
    elif is_valid and filled_count > 0: 
        return f'Grid valid, but needs {17 - filled_count} more cells (minimum 17)'
    else: 
        return ''


def get_progress_message(wrong_count, is_complete): 
    if is_complete: 
        return '🎉 Perfect! You solved it correctly!'
    elif wrong_count > 0: 
        return f'{wrong_count} incorrect cell(s)'
    else: 
        return ''

def start(request):
    if request.method == 'POST':
        level_form = LevelForm(request.POST)
        if level_form.is_valid():
            level = level_form.cleaned_data.get('level').lower()
            queryset = Grid.objects.filter(difficulty=level, is_public=True)

            if queryset.exists():
                random_grid = choice(queryset)
                return redirect('to_solve', id=random_grid.id)
            else:
                error = f'No {level} puzzles found in database.'
                return render(request, 'start.html', {'level_form': level_form, 'error': error})

    level_form = LevelForm()
    return render(request, 'start.html', {'level_form': level_form})

def new(request):
    if request.method == 'POST': 
        form = SudokuForm(request.POST)
        if form.is_valid(): 
            data = form.cleaned_data
            selected_difficulty = data.get('difficulty')

            grid_dict = {f"{r}{c}": data.get(f"{r}{c}") or "." for r in "ABCDEFGHI" for c in "123456789"}
            grid_string = "".join(grid_dict.values())

            if not is_valid_input(grid_dict): 
                messages.error(request, "Invalid Grid: Duplicate numbers found in a row, column, or block!")
                return render(request, 'new.html', {'form': form})

            solution = solve(grid_string)
            if not solution: 
                messages.error(request, "This puzzle has no possible solution!")
                return render(request, 'new.html', {'form': form})

            new_grid = Grid.objects.create(
                grid=grid_string,
                difficulty=selected_difficulty,
                created_by=request.user if request.user.is_authenticated else None,
                is_public=True
            )
            messages.success(request, f"Puzzle created successfully! ID: {new_grid.id}")
            return redirect('to_solve', id=new_grid.id)
    else: 
        form = SudokuForm()

    return render(request, 'new.html', {'form': form})


def to_solve(request, id):
    grid_obj = get_object_or_404(Grid, pk=id)
    initial_data = {}
    rows, cols = "ABCDEFGHI", "123456789"
    for i, char in enumerate(grid_obj.grid): 
        if char != '':
            field_name = f"{rows[i // 9]}{cols[i % 9]}"
            initial_data[field_name] = char
    form = SudokuForm(initial=initial_data)

    return render(request, 'solve.html', {
        'id': grid_obj.id,
        'form': form,
        'description': grid_obj
    })


def check_solution(request, id):
    grid_obj = get_object_or_404(Grid, pk=id)
    solution = solve(grid_obj.grid)

    wrong_cells = []
    correct_cells = []

    if request.method == 'POST': 
        for key in solution.keys(): 
            user_val = request.POST.get(key)
            if user_val: 
                if user_val != solution[key]: 
                    wrong_cells.append(key)
                else: 
                    correct_cells.append(key)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest': 
            return JsonResponse({
                'wrong_cells': wrong_cells,
                'correct_cells': correct_cells,
                'is_complete': len(wrong_cells) == 0 and len(correct_cells) == 81
            })

    form = SudokuForm(request.POST)
    return render(request, 'solve.html', {
        'id': id,
        'form': form,
        'wrong_cells': wrong_cells,
        'description': grid_obj
    })

def solved(request, id):
    grid_obj = get_object_or_404(Grid, pk=id)
    solved_grid = solve(grid_obj.grid)

    time_taken_seconds = request.POST.get('time_taken', '0') if request.method == 'POST' else '0'
    minutes = int(float(time_taken_seconds)) // 60
    seconds = int(float(time_taken_seconds)) % 60
    time_str = f'{minutes}m {seconds}s'

    if not solved_grid: 
        return render(request, 'solve.html', {'id': id, 'error': 'Unsolvable!'})

    return render(request, 'solved.html', {
        'grid': solved_grid,
        'original': grid_obj,
        'time_spent': time_str
    })


@login_required
def clear_grids(request):
    if request.method == 'POST':
        Grid.objects.all().delete()
        messages.success(request, 'Database cleared successfully!')
        return redirect('start')

    return render(request, 'start.html')


@login_required
def delete_puzzle(request, id) :
    grid_obj = get_object_or_404(Grid, pk=id)

    if grid_obj.created_by != request.user :
        messages.error(request, 'You can only delete your own puzzles!')
        return redirect('start')

    if request.method == 'POST' :
        grid_obj.delete()
        messages.success(request, f'Puzzle #{id} deleted successfully!')
        return redirect('my_puzzles')

    return render(request, 'delete.html', {'puzzle' :grid_obj})

def my_puzzles(request):
    user_puzzles = Grid.objects.filter(created_by=request.user).order_by('-date')
    return render(request, 'my_puzzles.html', {'puzzles': user_puzzles})

def login_view(request) :
    if request.method == 'POST' :
        username = request.POST.get('user')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None :
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('start')
        else :
            return render(request, 'login.html', {'error' :'Invalid username or password'})

    return render(request, 'login.html')


def logout_view(request) :
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('start')


def register_view(request) :
    if request.method == 'POST' :
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm :
            return render(request, 'register.html', {'error' :'Passwords do not match'})

        if User.objects.filter(username=username).exists() :
            return render(request, 'register.html', {'error' :'Username already exists'})

        if User.objects.filter(email=email).exists() :
            return render(request, 'register.html', {'error' :'Email already registered'})

        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)
        messages.success(request, f'Welcome, {user.username}! Your account has been created.')
        return redirect('start')

    return render(request, 'register.html')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GridSerializer

class SudokuListCreateAPI(APIView): 
    # GET: Get a random puzzle by difficulty (Replaces 'start' logic)
    def get(self, request): 
        level = request.query_params.get('level', 'easy').lower()
        queryset = Grid.objects.filter(difficulty=level)
        if queryset.exists(): 
            grid = choice(queryset)
            serializer = GridSerializer(grid)
            return Response(serializer.data)
        return Response({"error": "No puzzles found"}, status=status.HTTP_404_NOT_FOUND)

    # POST: Create a new puzzle (Replaces 'new' logic)
    def post(self, request): 
        serializer = GridSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SudokuSolveAPI(APIView): 
    def post(self, request, pk): 
        grid_obj = get_object_or_404(Grid, pk=pk)
        solution = solve(grid_obj.grid)
        user_input = request.data.get('grid_input')

        wrong_cells = [k for k, v in user_input.items() if v and v != solution.get(k)]

        return Response({
            "is_correct": len(wrong_cells) == 0 and "." not in user_input.values(),
            "wrong_cells": wrong_cells,
            "solution": solution if request.data.get('reveal') else None
        })