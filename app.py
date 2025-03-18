from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return '<h1>About Page</h1><p>This is a simple Flask web app.</p>'

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
