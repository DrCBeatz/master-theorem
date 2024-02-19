# mastertheorem/forms.py

from django import forms

class MasterTheoremForm(forms.Form):
    a = forms.IntegerField(label='a (number of subproblems)', min_value=1)
    b = forms.IntegerField(label='b (factor by which the problem size is reduced)', min_value=2)
    k = forms.IntegerField(label='k (exponent in the work done outside the recursive calls)', min_value=0)