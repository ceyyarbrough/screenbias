from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def hello_world():  # put application's code here
    return render_template('index.html', name='screenbias')
@app.route('/rightwing')
def rightwing():
    return render_template('right.html', name='rightscreenbias')
@app.route('/leftwing')
def leftwing():
    return render_template('left.html', name='leftscreenbias')
@app.route('/centerwing')
def centerwing():
    render_template('center.html', name='centerscreenbias')


if __name__ == '__main__':
    app.run()
