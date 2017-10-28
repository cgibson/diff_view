from flask import Flask, send_from_directory, request
from json import dumps
from repo_diff import *

REPO_URL = 'git@bitbucket.org:cowriterie/anh.git'
REPO_PATH = os.path.expandvars('$HOME/.diffview_repo')


@app.route('/')
def index():
    return send_from_directory('html', 'index.html')


@app.route('/js/<path:path>')
def javascript(path):
    return send_from_directory('js', path)


@app.route('/css/<path:path>')
def css(path):
    return send_from_directory('css', path)


@app.route('/generate')
def generate():
    ref_a = request.args['ref_a']
    ref_b = request.args['ref_b']

    diff = diff_from_sha(REPO_PATH, ref_a, ref_b, word_diff=True)
    markdown = generate_diff_markdown(diff)
    return markdown


@app.route('/refresh')
def refresh():
    refresh_repository(REPO_PATH)
    return dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/branches')
def branches():
    branches = branch_list(REPO_PATH)
    branches = [branch.strip() for branch in branches if branch.strip()]
    return dumps(branches)
