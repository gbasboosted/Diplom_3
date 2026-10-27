import secrets
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class SecretText:
    """Значение поля, которое не попадает в параметры шагов Allure."""
    value: str = field(repr=False)


@dataclass(frozen=True)
class UserData:
    email: str
    name: str
    password: SecretText = field(repr=False)

    def as_payload(self):
        return {"email": self.email, "name": self.name, "password": self.password.value}


def make_user():
    identifier = uuid4().hex
    return UserData(
        email=f"stellar-ui-{identifier}@example.com",
        name=f"UI {identifier[:8]}",
        password=SecretText(secrets.token_urlsafe(18)),
    )
