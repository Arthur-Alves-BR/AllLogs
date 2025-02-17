import pytest

from app.core.auth.password import is_valid_password


@pytest.mark.parametrize(
    ("password", "expected_exception", "expected_message"),
    [
        ("Abc1!", ValueError, ["The password is too short"]),
        ("abc123!@", ValueError, ["The password must contain at least one uppercase letter"]),
        ("ABC123!@", ValueError, ["The password must contain at least one lowercase letter"]),
        ("Abcdef!@", ValueError, ["The password must contain at least one digit"]),
        ("Abcdef12", ValueError, ["The password must contain at least one special character"]),
        (
            "abcdef",
            ValueError,
            [
                "The password is too short",
                "The password must contain at least one uppercase letter",
                "The password must contain at least one digit",
                "The password must contain at least one special character",
            ],
        ),
    ],
)
def test_is_valid_password_invalid(password, expected_exception, expected_message):
    with pytest.raises(expected_exception) as exc_info:
        is_valid_password(password)
    assert exc_info.value.args[0] == expected_message


@pytest.mark.parametrize(
    "password",
    [
        "Abc123!@",
        "StrongP@ssword1",
        "Valid123$",
        "PythonRocks9!",
    ],
)
def test_is_valid_password_valid(password):
    assert is_valid_password(password) == password
