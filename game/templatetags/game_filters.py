from django import template

register = template.Library()

@register.filter
def index(sequence, position):
    return sequence[position]


@register.filter
def index_flat(grid_data, position):
    ...
@register.filter
def get_grid_value(grid_data, coordinates):
    row_index = coordinates // 9
    col_index = coordinates % 9
    return grid_data[row_index][col_index]