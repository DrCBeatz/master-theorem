# mastertheorem/views.py

from django.shortcuts import render
from .master_theorem import evaluate_master_theorem, calculate_plot_data
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EvaluateMasterTheoremSerializer
from rest_framework import generics
from .models import Algorithm
from .serializers import AlgorithmSerializer

def frontend(request):
    return render(request, "index.html")

class EvaluateMasterTheoremAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EvaluateMasterTheoremSerializer(data=request.data)
        if serializer.is_valid():
            a = serializer.validated_data['a']
            b = serializer.validated_data['b']
            k = serializer.validated_data['k']
            complexity, case, recurrence_relation, regularity_condition_met = evaluate_master_theorem(a, b, k)
            
            # Calculate plot data
            plot_data = calculate_plot_data(a, b, k)
            
            data = {
                'complexity': complexity,
                'case': case,
                'recurrence_relation': recurrence_relation,
                'regularity_condition_met': regularity_condition_met,
                'plot_data': plot_data,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
    
class AlgorithmList(generics.ListAPIView):
    queryset = Algorithm.objects.all().order_by('id')
    serializer_class = AlgorithmSerializer