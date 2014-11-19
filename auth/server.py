from flask import Flask, render_template, request, make_response, redirect, url_for
app = Flask(__name__)

import sqlalchemy
engine = sqlalchemy.create_engine('postgres://app:app@localhost:5432/postgres', convert_unicode=True)

@app.route('/')
def hello():
	#return 'helloworld'
	if request.method == 'GET':
		return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		resp = make_response(str(request.form))

		resp.set_cookie('username', request.form['username'])
		resp.set_cookie('password', request.form['password'])

		return resp
	else:
		return render_template(
			'login.html',
			loggedIn=request.cookies.get('username'),
			username=request.cookies.get('username', 'guest'),
			password=request.cookies.get('password', 'none'),
		)

@app.route('/logout', methods=['GET'])
def logout():
	resp = redirect(url_for('hello'))
	resp.set_cookie(
		'username', '',
		expires='Thu, 01 Jan 1970 00:00:00 GMT'
	)
	resp.set_cookie(
		'password', '',
		expires='Thu, 01 Jan 1970 00:00:00 GMT'
	)
	return resp

if __name__ == '__main__':
	app.run(debug=True)
