from datetime import datetime
from app import db


recipe_ingredient = db.Table('recipe_ingredient',
                    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
                    db.Column('measure_id', db.Integer, db.ForeignKey('measure.id')),
                    db.Column('measure_qty_id', db.Integer, db.ForeignKey('measure_qty.id')),
                    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id')))


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    recipe = db.relationship('Recipe', backref='title', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(840))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    recipe_ingredient = db.relationship('Ingredient', secondary=recipe_ingredient,
                                        backref=db.backref('measure', lazy='dynamic'), cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Recipe {self.body}>'


class Measure(db.Model):
    __tablename__ = 'measure'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120))
    recipe_ingredient = db.relationship('Recipe', secondary=recipe_ingredient,
                                        backref=db.backref('recipes', lazy='dynamic'), cascade="all, delete-orphan")


class MeasureQty(db.Model):
    __tablename__ = 'measure_qty'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    recipe_ingredient = db.relationship('Recipe', secondary=recipe_ingredient,
                                        backref=db.backref('recipes', lazy='dynamic'), cascade="all, delete-orphan")


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    calories = db.Column(db.Integer)
    recipe_ingredient = db.relationship('Recipe', secondary=recipe_ingredient,
                                        backref=db.backref('recipes', lazy='dynamic'), cascade="all, delete-orphan")
