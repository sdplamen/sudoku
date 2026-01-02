from rest_framework import serializers
from .models import Grid
from .sudoku import solve, is_valid_input


class GridSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grid
        fields = ['id', 'grid', 'difficulty', 'date']

    def validate(self, data):
        grid_string = data.get('grid')
        rows, cols = 'ABCDEFGHI', '123456789'
        grid_dict = {f"{rows[i // 9]}{cols[i % 9]}" :char for i, char in enumerate(grid_string)}

        if not is_valid_input(grid_dict) :
            raise serializers.ValidationError('Duplicate numbers found in row, column, or block.')

        if not solve(grid_string) :
            raise serializers.ValidationError('This puzzle is unsolvable.')

        return data