import pytest
from datetime import datetime, timedelta
from app import app, db
from app.models import User, Recipe


class TestBD:
    def setup(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        assert u.check_password('dog') is False
        assert u.check_password('cat') is True

    def test_add_users(self):
        user_1 = User(username='john', email='john@example.com')
        user_2 = User(username='susan', email='susan@example.com')
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()
        assert user_1.recipe.all() == []
        assert user_2.recipe.all() == []

    def test_add_and_remove_recipe_to_user(self):
        user_1 = User(username='john', email='john@example.com')
        db.session.add(user_1)
        db.session.commit()
        recipe_1 = Recipe(title='Strawberry pie')
        user_1.add_recipe(recipe_1)
        assert user_1.recipe.count() == 1

        user_1.remove_recipe(recipe_1)
        db.session.commit()
        assert user_1.recipe.count() == 0





