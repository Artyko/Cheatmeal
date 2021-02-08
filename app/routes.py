from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, RecipeForm
from app.models import User, Recipe


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data,
                        description=form.description.data,
                        user_id=current_user.id)
        db.session.add(recipe)
        db.session.commit()
        flash(_('Your recipe is now live!'))
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    recipes = current_user.show_recipes().paginate(
        page, app.config['RECIPES_PER_PAGE'], False)
    next_url = url_for('index', page=recipes.next_num) \
        if recipes.has_next else None
    prev_url = url_for('index', page=recipes.prev_num) \
        if recipes.has_prev else None
    return render_template('index.html', title='Home',
                           form=form, recipes=recipes.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title=_('Sign In'), form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('login'))
    return render_template('register.html', title=_('Register'), form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    recipes = user.recipe.order_by(Recipe.timestamp.desc()).paginate(
        page, app.config['RECIPES_PER_PAGE'], False)
    next_url = url_for('index', page=recipes.next_num) \
        if recipes.has_next else None
    prev_url = url_for('index', page=recipes.prev_num) \
        if recipes.has_prev else None
    return render_template('user.html', user=user, recipes=recipes.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.timestamp.desc()).paginate(
        page, app.config['RECIPES_PER_PAGE'], False)
    next_url = url_for('index', page=recipes.next_num) \
        if recipes.has_next else None
    prev_url = url_for('index', page=recipes.prev_num) \
        if recipes.has_prev else None
    return render_template('index.html', title=_('Explore'), recipes=recipes.items,
                           next_url=next_url, prev_url=prev_url)
