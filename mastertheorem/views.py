# mastertheorem/views.py

from django.shortcuts import render
from .forms import MasterTheoremForm
from .master_theorem import evaluate_master_theorem, plot_master_theorem
from django.utils.crypto import get_random_string

def evaluate_view(request):
    # Define default values for the form
    default_values = {'a': 1, 'b': 2, 'c': 0}

    if request.method == 'POST':
        form = MasterTheoremForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            k = form.cleaned_data['c']
            complexity, case = evaluate_master_theorem(a, b, k)

            # Generate a random filename for the plot
            filename = f"plot_{get_random_string(8)}.png"
            plot_url = plot_master_theorem(a, b, k, filename)

            return render(request, 'evaluate_master_theorem.html', {
                'complexity': complexity,
                'case': case,
                'plot_url': plot_url,
                'form': form
            })
    else:
        form = MasterTheoremForm(initial=default_values)
    return render(request, 'evaluate_master_theorem.html', {'form':form})