# mastertheorem/tests/test_serializers.py

import pytest
from mastertheorem.models import Algorithm
from mastertheorem.serializers import AlgorithmSerializer, EvaluateMasterTheoremSerializer

@pytest.mark.django_db
def test_evaluate_master_theorem_serializer_valid_data():
    valid_data = {'a': 2, 'b': 2, 'k': 1}
    serializer = EvaluateMasterTheoremSerializer(data=valid_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_data

@pytest.mark.django_db
def test_evaluate_master_theorem_serializer_invalid_data():
    invalid_data = {'a': 0, 'b': 1, 'k': -1}
    serializer = EvaluateMasterTheoremSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'a' in serializer.errors
    assert 'b' in serializer.errors
    assert 'k' in serializer.errors

@pytest.mark.django_db
def test_algorithm_serializer():
    # Create an instance of the Algorithm model
    algorithm = Algorithm.objects.create(
        name="Test Algorithm",
        description="A test algorithm description.",
        python_code="def test_algorithm(): pass"
    )

    # Serializer the algorithm instance
    serializer = AlgorithmSerializer(instance=algorithm)

    # Check tht the serialized data matches what is expected
    assert serializer.data['name'] == "Test Algorithm"
    assert serializer.data['description'] == "A test algorithm description."
    assert serializer.data['python_code'] == "def test_algorithm(): pass"
    assert 'id' in serializer.data # Check if 'id' is included in the serialized data