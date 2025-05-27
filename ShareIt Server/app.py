from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from trip import trip_apis

app = Flask(__name__)

app.secret_key = "my_super_secret_key_2"

app.config['DEBUG'] = True

app.register_blueprint(trip_apis, url_prefix='/api/trip')

@app.route('/')
def home_page():  # put application's code here
    if 'username' not in session:
        return redirect(url_for('login'))

    app.logger.debug(session['username'])
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home_page'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


if __name__ == '__main__':
    app.run()
