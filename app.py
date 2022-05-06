import json
import os.path
from flask import Flask, redirect, render_template, request, url_for, flash, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = '102931239123912nienfi1i'
STATIC_PATH = 'static/user_files'


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
            f.save(f'{STATIC_PATH}/{full_name}')
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
        return render_template('your-url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    filename = urls[code]['file']
                    return redirect(url_for('static', filename=f'user_files/{filename}'))
    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404