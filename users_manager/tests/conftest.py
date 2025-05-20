import pytest

from employees.services import organization as services


@pytest.fixture
def mock_request(monkeypatch):
    def _mock_request(mocked_response):
        async def _mocked_function(method, url, headers=None, data=None):
            return {"body": mocked_response}

        monkeypatch.setattr(
            services, "make_request_with_error_handling", _mocked_function
        )

    return _mock_request
