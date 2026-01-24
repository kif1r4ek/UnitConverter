# UnitConverter Test Suite

This directory contains comprehensive unit and integration tests for the UnitConverter API.

## Test Structure

```
tests/
├── unit/                       # Unit tests (isolated component tests)
│   ├── test_length.py         # Length conversion service tests
│   ├── test_temperature.py    # Temperature conversion service tests
│   ├── test_weight.py         # Weight conversion service tests
│   ├── test_validators.py     # Domain model validators tests
│   ├── test_exceptions.py     # Custom exceptions tests
│   └── test_redis_service.py  # Redis service tests
├── integration/                # Integration tests (API endpoints)
│   ├── test_api_length.py     # Length API endpoint tests
│   ├── test_api_temperature.py # Temperature API endpoint tests
│   ├── test_api_weight.py     # Weight API endpoint tests
│   ├── test_api_health.py     # Health check endpoint tests
│   ├── test_middleware.py     # Middleware tests
│   └── test_error_handlers.py # Error handler tests
├── conftest.py                 # Shared fixtures and configuration
└── README.md                   # This file
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test Categories

**Unit tests only:**
```bash
pytest -m unit
```

**Integration tests only:**
```bash
pytest -m integration
```

**Redis-dependent tests only:**
```bash
pytest -m redis
```

**Exclude Redis tests (when Redis is not available):**
```bash
pytest -m "not redis"
```

### Run Specific Test File

```bash
pytest tests/unit/test_length.py
```

### Run Specific Test Class

```bash
pytest tests/unit/test_length.py::TestLengthConversions
```

### Run Specific Test

```bash
pytest tests/unit/test_length.py::TestLengthConversions::test_meters_to_kilometers
```

## Test Markers

Tests are marked with the following pytest markers:

- `@pytest.mark.unit` - Unit tests (no external dependencies)
- `@pytest.mark.integration` - Integration tests (test multiple components)
- `@pytest.mark.redis` - Tests requiring Redis connection
- `@pytest.mark.slow` - Tests that take longer to execute

## Test Coverage

### Unit Tests Coverage

**Conversion Services (100% coverage):**
- ✅ Length conversions (linear and area units)
- ✅ Temperature conversions (Celsius, Fahrenheit, Kelvin)
- ✅ Weight conversions (metric and imperial)
- ✅ Decimal rounding behavior
- ✅ Edge cases (zero, negative, very large/small values)
- ✅ Exception handling

**Domain Models (100% coverage):**
- ✅ PositiveValueValidator for length/weight
- ✅ Field validation
- ✅ Pydantic model behavior

**Custom Exceptions (100% coverage):**
- ✅ ConversionError
- ✅ UnsupportedUnitError
- ✅ DimensionalityConversionError
- ✅ NegativeValueError
- ✅ Exception hierarchy

**Redis Service (100% coverage):**
- ✅ History management (add, get, clear)
- ✅ Cache operations (set, get, delete)
- ✅ Key generation
- ✅ TTL and limits
- ✅ Error handling

### Integration Tests Coverage

**API Endpoints:**
- ✅ POST /length/convert
- ✅ POST /temperature/convert
- ✅ POST /weight/convert
- ✅ GET /length/history, /temperature/history, /weight/history
- ✅ DELETE /length/history, /temperature/history, /weight/history
- ✅ GET / (home page)
- ✅ GET /health (health check)

**Middleware:**
- ✅ LoggingMiddleware request/response logging
- ✅ Request ID generation
- ✅ Duration tracking
- ✅ Error handling

**Error Handlers:**
- ✅ ConversionError handling (400)
- ✅ ValidationError handling (422)
- ✅ Generic Exception handling (500)
- ✅ Error response formats

## Test Fixtures

Common fixtures are defined in `conftest.py`:

- `mock_redis` - Mocked Redis client
- `redis_service` - RedisService with mocked Redis
- `client` - FastAPI test client
- `mock_user_key` - Sample user key for testing
- `sample_length_conversion` - Sample length conversion data
- `sample_temperature_conversion` - Sample temperature conversion data
- `sample_weight_conversion` - Sample weight conversion data

## Writing New Tests

### Unit Test Example

```python
import pytest
from app.services.length import convert_length
from app.domain.units.length import UnitsLength

@pytest.mark.unit
def test_meters_to_kilometers():
    """Test conversion from meters to kilometers."""
    result = convert_length(1000, UnitsLength.M, UnitsLength.KM)
    assert result == 1.0
```

### Integration Test Example

```python
import pytest

@pytest.mark.integration
def test_length_conversion_endpoint(client):
    """Test length conversion API endpoint."""
    response = client.post(
        "/length/convert",
        json={
            "value": 1000,
            "from_unit": "m",
            "to_unit": "km",
            "decimals": 2
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 1.0
```

## Continuous Integration

Tests are designed to run in CI/CD pipelines. Use the following command for CI:

```bash
pytest -v --tb=short --disable-warnings
```

## Test Data

All test data uses realistic values and scenarios:
- Real-world conversion examples
- Edge cases (zero, negatives, very large/small)
- Boundary conditions
- Error scenarios

## Dependencies

Test dependencies are included in `requirements.txt`:
- pytest >= 9.0.2
- pytest-asyncio (for async tests)
- httpx (for FastAPI TestClient)
- unittest.mock (standard library)

## Troubleshooting

### Tests Failing Due to Redis

If Redis is not available, skip Redis tests:
```bash
pytest -m "not redis"
```

### Import Errors

Ensure you're running tests from the project root:
```bash
cd /path/to/UnitConverter
pytest
```

### Async Test Issues

Make sure `pytest-asyncio` is installed and `asyncio_mode = auto` is set in `pytest.ini`.

## Best Practices

1. **Isolation**: Unit tests should not depend on external services
2. **Mocking**: Use mocks for external dependencies (Redis, databases)
3. **Clarity**: Test names should clearly describe what is being tested
4. **Coverage**: Aim for high test coverage (>90%)
5. **Speed**: Unit tests should be fast; integration tests can be slower
6. **Assertions**: Each test should have clear, specific assertions

## Contributing

When adding new features:
1. Write unit tests first (TDD approach)
2. Add integration tests for API endpoints
3. Update this README if adding new test categories
4. Ensure all tests pass before committing

## License

Same as the main project.
