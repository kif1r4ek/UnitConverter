# Testing Quick Start Guide

## Installation

1. **Install test dependencies**:
```bash
pip install -r requirements.txt
```

This includes:
- pytest (test framework)
- pytest-asyncio (async test support)
- pytest-cov (coverage reporting)

## Running Tests

### Basic Commands

**Run all tests**:
```bash
pytest
```

**Run with verbose output**:
```bash
pytest -v
```

**Run with even more detail**:
```bash
pytest -vv
```

**Run tests and show print statements**:
```bash
pytest -s
```

### Test Selection

**Run only unit tests** (fast, no external dependencies):
```bash
pytest -m unit
```

**Run only integration tests**:
```bash
pytest -m integration
```

**Skip Redis-dependent tests** (when Redis is not available):
```bash
pytest -m "not redis"
```

**Run specific test file**:
```bash
pytest tests/unit/test_length.py
```

**Run specific test class**:
```bash
pytest tests/unit/test_length.py::TestLengthConversions
```

**Run specific test function**:
```bash
pytest tests/unit/test_length.py::TestLengthConversions::test_meters_to_kilometers
```

**Run tests by name pattern**:
```bash
# Run all tests with "temperature" in the name
pytest -k temperature

# Run all tests with "negative" in the name
pytest -k negative
```

### Coverage Reports

**Run tests with coverage**:
```bash
pytest --cov=app
```

**Generate HTML coverage report**:
```bash
pytest --cov=app --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

**Coverage with missing lines**:
```bash
pytest --cov=app --cov-report=term-missing
```

**Generate multiple report formats**:
```bash
pytest --cov=app --cov-report=html --cov-report=term --cov-report=xml
```

### Output Control

**Quiet mode** (less output):
```bash
pytest -q
```

**Show only test names** (collect tests without running):
```bash
pytest --collect-only
```

**Show test durations** (identify slow tests):
```bash
pytest --durations=10
```

**Stop at first failure**:
```bash
pytest -x
```

**Stop after N failures**:
```bash
pytest --maxfail=3
```

**Re-run failed tests** (after first run):
```bash
pytest --lf  # last failed
pytest --ff  # failed first, then all
```

## Common Workflows

### Development Workflow

1. **Quick check** (unit tests only):
```bash
pytest -m unit -q
```

2. **Full validation** (all tests with coverage):
```bash
pytest --cov=app --cov-report=term-missing
```

3. **Before commit** (all tests, stop on failure):
```bash
pytest -x -v
```

### Debugging Tests

**Run single failing test with output**:
```bash
pytest tests/unit/test_length.py::TestLengthConversions::test_meters_to_kilometers -s -vv
```

**Show local variables on failure**:
```bash
pytest -l
```

**Drop into debugger on failure**:
```bash
pytest --pdb
```

**Start debugger at test start**:
```bash
pytest --trace
```

### Continuous Integration

**CI/CD command** (suitable for automation):
```bash
pytest -v --tb=short --disable-warnings --cov=app --cov-report=xml
```

## Test Statistics

Current test suite includes:
- **Total tests**: 250+
- **Unit tests**: 130+
- **Integration tests**: 120+
- **Test files**: 13

### Breakdown by Component

| Component | Test Count |
|-----------|------------|
| Length conversions | 35+ |
| Temperature conversions | 44+ |
| Weight conversions | 37+ |
| Redis service | 25+ |
| Validators | 10+ |
| Exceptions | 23+ |
| API endpoints | 50+ |
| Middleware | 10+ |
| Error handlers | 16+ |

## Expected Output

### Successful Test Run
```
============================= test session starts ==============================
platform win32 -- Python 3.12.0, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\gosha\.claude-worktrees\UnitConverter\elated-yonath
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.12.0, asyncio-1.3.0
asyncio: mode=Mode.AUTO
collected 250 items

tests/unit/test_length.py ..................................... [ 15%]
tests/unit/test_temperature.py ...................................... [ 33%]
tests/unit/test_weight.py ..................................... [ 48%]
tests/unit/test_validators.py .......... [ 52%]
tests/unit/test_exceptions.py ........................ [ 62%]
tests/unit/test_redis_service.py ......................... [ 72%]
tests/integration/test_api_length.py .................. [ 80%]
tests/integration/test_api_temperature.py ............... [ 86%]
tests/integration/test_api_weight.py .................. [ 93%]
tests/integration/test_api_health.py ... [ 94%]
tests/integration/test_middleware.py .......... [ 98%]
tests/integration/test_error_handlers.py ................ [100%]

========================== 250 passed in 5.42s ==============================
```

### With Coverage
```
========================== 250 passed in 5.42s ==============================

---------- coverage: platform win32, python 3.12.0 -----------
Name                                    Stmts   Miss  Cover
-----------------------------------------------------------
app/services/length.py                     15      0   100%
app/services/temperature.py                15      0   100%
app/services/weight.py                     15      0   100%
app/services/redis_service.py              85      2    98%
app/domain/exceptions.py                   20      0   100%
app/domain/models/validator.py             10      0   100%
app/api/controller_length.py               45      1    98%
app/api/controller_temperature.py          45      1    98%
app/api/controller_weight.py               45      1    98%
app/core/middleware.py                     25      0   100%
app/core/error_handlers.py                 30      0   100%
-----------------------------------------------------------
TOTAL                                     350      5    98%
```

## Troubleshooting

### Problem: "ModuleNotFoundError"
**Solution**: Make sure you're in the project root directory:
```bash
cd /path/to/UnitConverter
pytest
```

### Problem: "fixture not found"
**Solution**: Ensure `conftest.py` exists in the tests directory and imports are correct.

### Problem: "Redis connection failed"
**Solution**: Skip Redis tests or ensure Redis is running:
```bash
# Skip Redis tests
pytest -m "not redis"

# Or start Redis
docker-compose up -d redis
```

### Problem: Tests are slow
**Solution**: Run only unit tests (they're fast):
```bash
pytest -m unit
```

Or parallelize with pytest-xdist:
```bash
pip install pytest-xdist
pytest -n auto  # auto-detect CPU count
```

### Problem: Import errors with async tests
**Solution**: Ensure pytest-asyncio is installed:
```bash
pip install pytest-asyncio
```

## Best Practices

1. **Run tests frequently** - Catch issues early
2. **Run unit tests first** - They're fast and catch most issues
3. **Check coverage** - Aim for >90% coverage
4. **Fix tests immediately** - Don't let them stay broken
5. **Update tests with code** - Keep them in sync

## IDE Integration

### VS Code
Add to `.vscode/settings.json`:
```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ]
}
```

### PyCharm
1. Go to Settings → Tools → Python Integrated Tools
2. Set Default test runner to "pytest"
3. Right-click test file → Run 'pytest in...'

## Next Steps

1. Read `tests/README.md` for detailed test documentation
2. Read `TEST_SUMMARY.md` for comprehensive overview
3. Explore test files to understand patterns
4. Add new tests as you add features
5. Maintain high coverage (>90%)

## Quick Reference

| Command | Description |
|---------|-------------|
| `pytest` | Run all tests |
| `pytest -m unit` | Run unit tests only |
| `pytest -m integration` | Run integration tests only |
| `pytest -v` | Verbose output |
| `pytest -s` | Show print statements |
| `pytest -x` | Stop at first failure |
| `pytest -k pattern` | Run tests matching pattern |
| `pytest --cov=app` | Run with coverage |
| `pytest --collect-only` | List tests without running |
| `pytest --lf` | Re-run last failed tests |

Happy testing! 🧪✅
