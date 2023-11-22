from flask import Flask, send_file, request, session, render_template, Response, jsonify, make_response
from flask_session import Session 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os 
import json
from modules.utils import load_config
from functools import wraps
import jwt
import pandas as pd 
from datetime import datetime, timezone, timedelta

PRJ_DIR = os.path.dirname(__file__)
os.chdir(PRJ_DIR)

save_dir = os.path.join(PRJ_DIR, 'data')
os.makedirs(save_dir, exist_ok=True)

app = Flask(__name__)

aws_db = {
    'user': 'anndaeu', 
    'password': 'anndaeu123', 
    'host': 'database-1.cc6wxqlyu039.ap-southeast-2.rds.amazonaws.com',
    'port': 3306, 
    'database': 'test_db'
}
   
# Setup database
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{aws_db['user']}:{aws_db['password']}@{aws_db['host']}:{aws_db['port']}/{aws_db['database']}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

users = []

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), db.ForeignKey('users.username'))
    img_path = db.Column(db.String(128), unique=True, nullable=False)
    result = db.Column(db.String(64), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/')
def main():
    return 'Flask is working...'

@app.route('/check_user', methods=['POST'])
def check_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        return jsonify({'message': 'logged in successfully'}), 200
    return jsonify({'message': 'invalid username or password'}), 401

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'username already exists'}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'registered successfully'}), 201

@app.route('/fetch_image', methods=['POST'])
def fetch_image():
    data = request.get_json()
    return send_file(data['img_path'], mimetype='image/png')

# @app.route('/upload')
# def upload_page():
#     return render_template('upload.html')

@app.route('/save_result', methods=['POST'])
def save_result():
    file = request.files['image']
    data = request.form
    
    kst = timezone(timedelta(hours=9))
    capture_date = datetime.now(tz=kst).strftime("%Y%m%d_%H%M%S") # 현재 시간을 이미지 촬영 날짜로 사용

    if file:
        # Save the image file
        user_folder = os.path.join(save_dir, data['username']) 
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        
        img_path = os.path.join(user_folder, f'{capture_date}.png')
        file.save(img_path)
                
        # Insert the image data into the database
        new_image = Data(username=data['username'], img_path=img_path, result = data['result'])
        db.session.add(new_image)
        db.session.commit()
        
        return "The image was successfully saved.", 200
    else: 
        return "No file was uploaded.", 400
 
@app.route('/select_result', methods=['POST'])
def select_result():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        
        user_logs = Data.query.filter_by(username=data['username']).all()
        
        ret = [{'id': user.id, 'username': user.username, 'img_path': user.img_path, 'result': user.result} for user in user_logs]
        return jsonify(ret), 200
    return jsonify({'message': 'invalid username or password'}), 401
 
 
@app.route('/send_data', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        folder_name = request.values['save_folder']
        idx = str(request.values['index']).zfill(7)
        line = request.values['data']
    
        folder_dir = os.path.join(save_dir, folder_name)    
        os.makedirs(folder_dir, exist_ok=True)
        file_path = os.path.join(folder_dir, f'data_{idx}.txt')
        
        with open(file_path, 'w', encoding='UTF-8') as f:
            f.write(line)
            
        response = {
            # 'request_id':request_id,
            'response': True,
        }
    else :
        response = {
            'response': False
        }

    return Response(
        json.dumps(response),
        mimetype='multipart/form-data')

if __name__ == "__main__":
    PRJ_DIR = os.path.dirname(__file__)
    os.chdir(PRJ_DIR)
    
    # config 
    CONFIG_PATH = os.path.join(PRJ_DIR, 'config/server.yaml')
    args = load_config(CONFIG_PATH)
    
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=args.port, debug=True) # debug: hot-reload 여부