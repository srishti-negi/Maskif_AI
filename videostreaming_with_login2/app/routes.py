from flask import render_template, Response, redirect, flash, request, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.camera import VideoCamera
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import time

@app.route('/') 
@app.route('/index')
def index():
    return render_template('index.html')

#@app.route('/success')
#@login_required
#def success():
#    #print(maskTF)
#    current_user.wearing_mask = maskTF 
#    db.session.commit()
#    return render_template('success.html')

@login_required
def gen(camera):
    curr_time = time.time()
    while time.time() < curr_time + 5:
        frame, wearmask = camera.get_frame()
        global maskTF 
        maskTF = wearmask
        print(maskTF)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
@login_required
def video_feed():
#    user = User.query.filter_by(id=current_user.get_id).first()
#    user.wearing_mask = False
#    db.session.add(user)
#    db.session.commit()
    return Response(gen(VideoCamera()), mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/success')
@login_required
def success():
    #print(maskTF)
    current_user.wearing_mask = maskTF 
    db.session.commit()
    return render_template('success.html')

@app.route('/check')
@login_required
def check():
    #print(maskTF)
    return render_template('maskdetection.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

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
        flash('You are registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
