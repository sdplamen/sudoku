from django.core.management import BaseCommand
from game.models import Grid

class Command(BaseCommand) :
    help = 'Display grids with dots for manual inspection'

    def handle(self, *args, **options) :
        grids = Grid.objects.all()

        self.stdout.write(self.style.WARNING(f'Found {grids.count()} grids in database'))

        for grid in grids :
            dot_count = grid.grid.count('.')
            if dot_count > 0 :
                self.stdout.write(f"Grid {grid.id}: {dot_count} empty cells (dots)")
                self.stdout.write(f"  Sample: {grid.grid[:27]}")

        self.stdout.write(self.style.SUCCESS('Done!'))