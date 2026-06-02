class Employee:
    company = "Linkific"

    def __init__(self, salary: float):
        self._salary = salary

    @property
    def salary(self):
        return self._salary

    @staticmethod
    def greet():
        return "Welcome"

    @classmethod
    def get_company(cls):
        return cls.company