import factory.fuzzy
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from app.models import Tasks

faker = FakerFactory.create()


@register(_name="tasks")
class TasksFactory(factory.Factory):
    class Meta:
        model = Tasks

    id = factory.LazyFunction(lambda: faker.random_int())
    name = factory.LazyFunction(lambda: faker.name())
    pomodoro_count = factory.LazyFunction(lambda: faker.random_int())
    category_id = factory.LazyFunction(lambda: faker.random_int())
    user_id = factory.LazyFunction(lambda: faker.random_int())
