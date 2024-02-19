# mastertheorem/views.py

from django.shortcuts import render
from .forms import MasterTheoremForm
from .master_theorem import evaluate_master_theorem

def evaluate_view(request):
    if request.method == 'POST':
        form = MasterTheoremForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            k = form.cleaned_data['c']
            complexity, case = evaluate_master_theorem(a, b, k)
            return render(request, 'evaluate_result.html', {
                'complexity': complexity,
                'case': case,
                'form': form
            })
    else:
        form = MasterTheoremForm()
    return render(request, 'evaluate_result.html', {'form':form})