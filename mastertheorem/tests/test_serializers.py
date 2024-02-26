import pytest
from mastertheorem.models import Algorithm
from mastertheorem.serializers import AlgorithmSerializer

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