| Concept | Purpose |
| :--- | :--- |
| **Naming Conventions** | Pytest auto-discovers files starting with `test_` or ending with `_test.py`, and functions starting with `test_`. |
| **Assertions & Exceptions** | Uses standard Python `assert` statements and `pytest.raises()` for exception validation. |
| **Fixtures (`@pytest.fixture`)** | Reusable setup/teardown code, state management, and dependency injection. |
| **Parameterization (`@pytest.mark.parametrize`)** | Run the same test function across multiple datasets without duplicating code. |
| **Markers (`@pytest.mark`)** | Categorize tests (e.g., `smoke`, `slow`, `integration`), skip tests, or mark expected failures (`xfail`). |
| **Mocking (`unittest.mock` / `pytest-mock`)** | Isolate external dependencies like APIs or databases. |