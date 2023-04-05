from sqlalchemy import true
import pytest
# import sys
# sys.path.append("tests")
from tests.add1 import add

# we can pass these fixtures to our test functions
@pytest.fixture
def fixture_func():
    return True




@pytest.mark.parametrize("num1, num2, result", [(1, 5, 6), (20, 41, 61), (0, 0, 0), (0, -10, -10)])

def test_add1(num1, num2, result):
    assert add(num1, num2) == result
