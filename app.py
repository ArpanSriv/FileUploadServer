import os
from datetime import datetime

import flask
from flask import Flask, render_template, jsonify, redirect, url_for, request

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


@app.route("/")
def index():
    return "Works ok"


@app.route('/upload', methods=['POST'])
def upload():
    print("Method called atleast")
    if request.method == 'POST':
        file = request.files['cert']

        if file and allowed_file(file.filename):
            team_name = request.form['team-name-hidden']
            reg_no = request.form['team-reg-no-hidden']

            folder_name = "{}_{}".format(team_name, reg_no)

            now = datetime.now()

            # filename = os.path.join(app.config['UPLOAD_FOLDER'],
            #                         "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))

            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], folder_name))

            folder_location = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)

            filename = os.path.join(folder_location, "Registration Certificate %s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))

            file.save(filename)

            response = flask.jsonify({"success": True})
            response.headers.add('Access-Control-Allow-Origin', 'http://aihackathon.in')
            response.headers.add('Access-Control-Allow-Headers', 'x-requested-with')
            return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='localhost')
