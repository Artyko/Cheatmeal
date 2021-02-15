from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.forms import EditProfileForm, RecipeForm
from app.models import User, Recipe
from app.main import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    recipes = current_user.show_recipes().paginate(
        page, current_app.config['RECIPES_PER_PAGE'], False)
    next_url = url_for('main.index', page=recipes.next_num) \
        if recipes.has_next else None
    prev_url = url_for('main.index', page=recipes.prev_num) \
        if recipes.has_prev else None
    return render_template('index.html', title='Home',
                           form=form, recipes=recipes.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    recipes = user.recipe.order_by(Recipe.timestamp.desc()).paginate(
        page, current_app.config['RECIPES_PER_PAGE'], False)
    next_url = url_for('main.user', page=recipes.next_num) \
        if recipes.has_next else None
    prev_url = url_for('main.user', page=recipes.prev_num) \
        if recipes.has_prev else None
    return render_template('user.html', user=user, recipes=recipes.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.timestamp.desc()).paginate(
        page, current_app.config['RECIPES_PER_PAGE'], False)
    next_url = url_for('main.index', page=recipes.next_num) \
        if recipes.has_next else None
    prev_url = url_for('main.index', page=recipes.prev_num) \
        if recipes.has_prev else None
    return render_template('index.html', title=_('Explore'), recipes=recipes.items,
                           next_url=next_url, prev_url=prev_url)
