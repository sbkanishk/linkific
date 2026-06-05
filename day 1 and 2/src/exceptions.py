class InvalidAgeError(Exception):
    pass


def validate_age(age: int):
    if age < 18:
        raise InvalidAgeError("Age must be at least 18")