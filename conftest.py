import pytest

@pytest.fixture
def sample_fixture():
    # Setup code
    print("\nSetup: Running before the test")
    yield
    # Teardown code
    print("\nTeardown: Running after the test")