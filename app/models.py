from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

recipe_ingredient = db.Table('recipe_ingredient',
                             db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
                             db.Column('measure_id', db.Integer, db.ForeignKey('measure.id')),
                             db.Column('measure_qty_id', db.Integer, db.ForeignKey('measure_qty.id')),
                             db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id')))


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    recipe = db.relationship('Recipe', backref='recipes', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def show_recipes(self):
        return Recipe.query.filter_by(user_id=self.id)


class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(840))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    recipes = db.relationship('Ingredient', secondary=recipe_ingredient,
                              primaryjoin=(recipe_ingredient.c.recipe_id == id),
                              secondaryjoin=(recipe_ingredient.c.ingredient_id == id),
                              backref=db.backref('ingredient', lazy='dynamic'), cascade="all")

    def __repr__(self):
        return f'<Recipe {self.title}>'

    def exist(self, recipe):
        return self.recipes.filter(recipe_ingredient.c.recipe_id == recipe.id).count() > 0

    def add_recipe(self, recipe):
        if not self.exist(recipe):
            self.recipes.append(recipe)

    def remove_recipe(self, recipe):
        if not self.exist(recipe):
            self.recipes.remove(recipe)


class Measure(db.Model):
    __tablename__ = 'measure'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120))
    recipe_ingredient = db.relationship('Recipe', secondary=recipe_ingredient,
                                        backref=db.backref('recipes_names', lazy='dynamic'), cascade="all")


class MeasureQty(db.Model):
    __tablename__ = 'measure_qty'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    recipe_ingredient = db.relationship('Recipe', secondary=recipe_ingredient,
                                        backref=db.backref('recipes_1', lazy='dynamic'), cascade="all")


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    calories = db.Column(db.Integer)
    recipe_ingredient = db.relationship('Recipe', secondary=recipe_ingredient,
                                        backref=db.backref('recipes_2', lazy='dynamic'), cascade="all")
