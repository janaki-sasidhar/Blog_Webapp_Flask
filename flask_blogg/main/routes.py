from flask import Blueprint , flash , render_template , redirect ,abort ,request
from flask_login import current_user , login_required
from flask_blogg.models import Post , User
main = Blueprint('main',__name__)
errors = Blueprint('errors',__name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        return render_template('index.html', posts=posts, title='Index', user=user)
    else:
        return render_template('index.html', posts=posts, title='Index')


@main.route('/about')
def about():
    return render_template('about.html')





@errors.app_errorhandler(404)
def error_404(e):
    return render_template("400.html"), 404


@errors.app_errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500
