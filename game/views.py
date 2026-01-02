from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Grid
from .forms import SudokuForm, LevelForm
from .sudoku import solve, is_valid_input
from random import choice


def start(request):
    if request.method == 'POST':
        level_form = LevelForm(request.POST)
        if level_form.is_valid():
            level = level_form.cleaned_data.get('level').lower()
            queryset = Grid.objects.filter(difficulty=level)

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
                return render(request, 'new.html', {'form' :form})

            solution = solve(grid_string)
            if not solution:
                messages.error(request, "This puzzle has no possible solution!")
                return render(request, 'new.html', {'form' :form})

            new_grid = Grid.objects.create(
                grid=grid_string,
                difficulty=selected_difficulty,
            )
            return redirect('to_solve', id=new_grid.id)
    else:
        form = SudokuForm()

    return render(request, 'new.html', {'form': form})


def to_solve(request, id):
    grid_obj = get_object_or_404(Grid, pk=id)
    initial_data = {}
    rows, cols = "ABCDEFGHI", "123456789"
    for i, char in enumerate(grid_obj.grid) :
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
    if request.method == 'POST':
        for key in solution.keys():
            user_val = request.POST.get(key)
            if user_val and user_val != solution[key]:
                wrong_cells.append(key)

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

    time_taken_seconds = request.POST.get('time_taken', 0)
    minutes = int(time_taken_seconds) // 60
    seconds = int(time_taken_seconds) % 60
    time_str = f'{minutes}m {seconds}s'

    if not solved_grid:
        return render(request, 'solve.html', {'id': id, 'error': 'Unsolvable!'})

    return render(request, 'solved.html', {
        'grid': solved_grid,
        'original': grid_obj,
        'time_spent': time_str
    })


def clear_grids(request):
    if request.method == 'POST':
        Grid.objects.all().delete()
        messages.success(request, 'Database cleared successfully!')
        return redirect('start')

    return render(request, 'start.html')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GridSerializer


class SudokuListCreateAPI(APIView) :
    # GET: Get a random puzzle by difficulty (Replaces 'start' logic)
    def get(self, request) :
        level = request.query_params.get('level', 'easy').lower()
        queryset = Grid.objects.filter(difficulty=level)
        if queryset.exists() :
            grid = choice(queryset)
            serializer = GridSerializer(grid)
            return Response(serializer.data)
        return Response({"error" :"No puzzles found"}, status=status.HTTP_404_NOT_FOUND)

    # POST: Create a new puzzle (Replaces 'new' logic)
    def post(self, request) :
        serializer = GridSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SudokuSolveAPI(APIView) :
    def post(self, request, pk) :
        grid_obj = get_object_or_404(Grid, pk=pk)
        solution = solve(grid_obj.grid)
        user_input = request.data.get('grid_input')

        wrong_cells = [k for k, v in user_input.items() if v and v != solution.get(k)]

        return Response({
            "is_correct" :len(wrong_cells) == 0 and "." not in user_input.values(),
            "wrong_cells" :wrong_cells,
            "solution" :solution if request.data.get('reveal') else None
        })