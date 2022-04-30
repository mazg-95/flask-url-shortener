import json
import os.path
from flask import Flask, redirect, render_template, request, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = '102931239123912nienfi1i'


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return 'This is a url shortener'

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save(full_name)
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
        return render_template('your-url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))