from django import forms


class LevelForm(forms.Form) :
    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class SudokuForm(forms.Form):
    difficulty = forms.ChoiceField(
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        widget=forms.Select(attrs={'class': 'form-control mb-3'})
    )
    def __init__(self, *args, **kwargs):
        super(SudokuForm, self).__init__(*args, **kwargs)
        rows = 'ABCDEFGHI'
        cols = '123456789'
        for r in rows:
            for c in cols:
                field_name = f'{r}{c}'
                self.fields[field_name] = forms.CharField(
                    widget=forms.TextInput(attrs={
                        'class' : 'cell',
                        'maxlength': '1',
                        'inputmode': 'numeric',
                        # 'pattern': '[1-9]',
                        'autocomplete': 'off'
                    }),
                    required=False
                )