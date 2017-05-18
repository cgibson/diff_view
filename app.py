from flask import Flask, send_from_directory, request
from json import dumps
from repo_diff import *

app = Flask(__name__)
app.debug = True

REPO_PATH = os.environ["REPO_PATH"]


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
    ref_a = request.args["ref_a"]
    ref_b = request.args["ref_b"]

    diff = diff_from_sha(REPO_PATH, ref_a, ref_b, word_diff=True)
    markdown = generate_diff_markdown(diff)
    return markdown


@app.route('/branches')
def branches():
    branches = branch_list(REPO_PATH)
    return dumps(branches)

if __name__ == '__main__':
    app.run()