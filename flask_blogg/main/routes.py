from flask import Blueprint , flash , render_template , redirect ,abort ,request , jsonify , url_for
from flask_login import current_user , login_required
from flask_blogg import db
import datetime
from sqlalchemy import func
from flask_blogg.models import Post , User , dailyRecord
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



@main.route("/myip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200




@main.route('/dailyrecord/',methods=["GET","POST"])
@login_required
def dailyrecord():
    if request.method=="POST":
        todaydate = datetime.date.today().strftime('%Y-%m-%d')
        dailyrecorddata = dailyRecord.query.filter(func.DATE(dailyRecord.date_posted) == todaydate).filter_by(userid=current_user.id).all()
        print(len(dailyrecorddata))
        if len(dailyrecorddata) == 0:
            print('i am here')
            if request.form['form_type']=='daily_record_data':
                morningwalk = int(request.form['morningWalk'])
                waterdrank = int(request.form['waterDrank'])
                breakfast = int(request.form['breakfast'])
                breakfast_calories = int(request.form['breakfastcalories'])
                lunch = int(request.form['lunch'])
                lunch_calories = int(request.form['lunchcalories'])
                dinner = int(request.form['dinner'])
                dinner_calories = int(request.form['dinnercalories'])
                nightwalk = int(request.form['nightWalk'])
                comments = request.form['comments']
                total_calories=breakfast_calories+dinner_calories+lunch_calories
                dailyrecord = dailyRecord(morningwalk=morningwalk , waterdrank=waterdrank , breakfast=breakfast, breakfast_calories=breakfast_calories,
                lunch=lunch,lunch_calories=lunch_calories,
                dinner=dinner,dinner_calories=dinner_calories,
                nightwalk=nightwalk,comment=comments,
                total_calories=total_calories,
                posted_or_not=1,userid=current_user.id)
                db.session.add(dailyrecord)
                db.session.commit()
                flash('data is uploaded successfully','success')
        else:
            print('i am in else')
            flash('You already filled the form today. You can only do it tomorrow','danger')
    return render_template('dailyrecord.html')


@errors.app_errorhandler(404)
def error_404(e):
    return render_template("400.html"), 404


@errors.app_errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


