# 회원수정 기능 구현
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User, Diary

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/Account_settings/', methods=('GET', 'POST'))
def Account_settings():
    username = g.user.username
    return render_template('profile/Account_Settings.html', username=username)

@bp.route('/Edit_profile/', methods=('GET', 'POST'))
def Edit_profile():
    return render_template('profile/Edit_Profile.html')


