from sklearn import svm
import joblib
import pickle
from app import app
from flask import request, jsonify
from dbse import *


@app.route('/train_harvest', methods=['POST', 'GET'])
def train_harvest():
    crop_id = request.json.get('crop_id')
    X, y = predict.predict_harvest(crop_id)
    model = svm.SVR(kernel='rbf')
    model.fit(X, y)
    joblib.dump(model, f'/static/harvest_model{crop_id}.z')
    return jsonify({
        'response': 'success'
    })


@app.route('/predict_harvest', methods=['POST'])
def predict_harvest():
    field_id = request.json.get('field_id')
    crop_id = request.json.get('crop_id')
    res = field.search_field(field_id=field_id)[0]
    input_date = res[6:10]
    try:
        f = open(f'./static/harvest_model{crop_id}.pkl', 'rb')
        model = pickle.load(f)
    except FileNotFoundError:
        model = svm.SVR(kernel='rbf')
        X, y = predict.predict_harvest(crop_id)
        model.fit(X, y)
        with open(f'./static/harvest_model{crop_id}.pkl', 'wb') as f:
            pickle.dump(model, f)
    harvest_weight = model.predict([input_date])
    return jsonify({
        'field_id': field_id,
        'crop_id': crop_id,
        'field_name': field.search_field(field_id=field_id)[0][1],
        'crop_name': crop.search_crop(crop_id=crop_id)[0][1],
        'harvest_weight': harvest_weight,
    })