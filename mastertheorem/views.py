# mastertheorem/views.py

import os
from django.conf import settings
from django.shortcuts import render
from .forms import MasterTheoremForm
from .master_theorem import evaluate_master_theorem, plot_master_theorem
from django.utils.crypto import get_random_string

from rest_framework import generics
from .models import Algorithm
from .serializers import AlgorithmSerializer

class AlgorithmList(generics.ListAPIView):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer

def evaluate_view(request):
    # Define default values for the form
    default_values = {'a': 1, 'b': 2, 'k': 0}

    if request.method == 'POST':
        form = MasterTheoremForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            k = form.cleaned_data['k']
            complexity, case = evaluate_master_theorem(a, b, k)

            # Directory where plot images are saved
            plots_directory = os.path.join(settings.BASE_DIR, 'static', 'plots')

            # Delete all existing .png files in the directory
            for filename in os.listdir(plots_directory):
                if filename.endswith(".png"):
                    file_path = os.path.join(plots_directory, filename)
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        print(f"Error deleting file {filename}: {e.strerror}")

            # Generate a new plot with a random filename
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

