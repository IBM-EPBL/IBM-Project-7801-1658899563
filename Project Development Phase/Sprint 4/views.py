from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Prediction,User
from . import db
import json
import pickle
import os
import pandas as pd

#importing model from pickle file
my_dir = os.path.dirname(__file__)
pickle_file_path = os.path.join(my_dir, 'static/IBM_RF_model.pickle')
with open(pickle_file_path, 'rb') as f:
    LRmodel = pickle.load(f)

views = Blueprint('views', __name__)

@views.route('/')
def home():
    reviews=db.engine.execute("Select first_name,last_name,text,rating from User Where not text='None' Order By rating DESC limit 3;")
    return render_template("home.html", user=current_user, reviews=reviews)

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    result=1
    display="none"
    reviewdisplay="block"
    reviewbtn="Update Review"
    userreview=""
    stars=0

    if current_user.text is None:
        reviewdisplay="none"
        reviewbtn="Publish"
    else:
        userreview=current_user.text
        stars=int(current_user.rating)

    if request.method == 'POST':
        if 'newprediction' in request.form:
            vmodel=request.form.get('vmodel')
            distance = request.form.get('distance')
            speed = request.form.get('speed')
            temp_inside = request.form.get('temp_inside')
            temp_outside = request.form.get('temp_outside')
            ac = request.form.get('ac')
            gas_type = request.form.get('gas_type')
            rain = request.form.get('rain')
            sun = request.form.get('sun')

            if len(vmodel) < 1:
                flash('Vehicle model field can\'t be empty.', category='error')
            elif len(distance) < 1:
                flash('Distance field can\'t be empty.', category='error')
            elif len(speed) < 1:
                flash('Speed field can\'t be empty.', category='error')
            elif len(temp_inside) < 1:
                flash('Engine temperature field can\'t be empty.', category='error')
            elif len(temp_outside) < 1:
                flash('Environment temperature field can\'t be empty.', category='error')
            elif gas_type is None:
                flash('Fuel Type is not selected.', category='error')
            elif ac is None:
                flash('AC field is not selected.', category='error')
            elif rain is None:
                flash('Rainy day field is not selected.', category='error')
            elif sun is None:
                flash('Sunny day field is not selected.', category='error')
            else:
                list=[[float(distance),float(speed),float(temp_inside),float(temp_outside),int(gas_type),int(ac),int(rain),int(sun)]]
                pred=pd.DataFrame(list)
                result=LRmodel.predict(pred)[0]
                
                new_pred = Prediction(
                    vmodel=vmodel,
                    distance=float(distance),
                    speed=float(speed),
                    temp_inside=float(temp_inside),
                    temp_outside=float(temp_outside),
                    gas_type=int(gas_type),
                    ac=int(ac),
                    rain=int(rain),
                    sun=int(sun),
                    consume=result,
                    user_id=current_user.id
                    )
                db.session.add(new_pred)
                db.session.commit()
                display="block"
                flash('Prediction successfull !', category='success')
        
        elif 'submitreview' in request.form:
            rating=request.form.get('rating')
            reviewtext=request.form.get('comment')

            if rating is None:
                flash('Rating is not selected.', category='error')
            elif len(reviewtext)<3:
                flash('Review is too short.', category='error')
            else:
                current_user.rating=int(rating)
                current_user.text=str(reviewtext)
                db.session.commit()
                reviewdisplay="block"
                reviewbtn="Update Review"
                userreview=reviewtext
                stars=int(rating)
                flash('Review posted!', category='success')

    return render_template("dashboard.html", user=current_user, prediction_result=result, display=display, reviewdisplay=reviewdisplay,userreview=userreview,reviewbtn=reviewbtn,stars=stars)


@views.route('/delete-pred', methods=['POST'])
def delete_pred():
    pred = json.loads(request.data)
    predId = pred['predID']
    pred = Prediction.query.get(predId)
    if pred:
        if pred.user_id == current_user.id:
            db.session.delete(pred)
            db.session.commit()
            flash('Prediction deleted!', category='error')
    return jsonify({})

@views.route('/delete-review', methods=['POST'])
def delete_review():
    cuser = json.loads(request.data)
    userId = cuser['userID']
    cuser = User.query.get(userId)
    if cuser:
        cuser.rating=None
        cuser.text=None
        db.session.commit()
        flash('Review deleted!', category='error')
    return jsonify({})
