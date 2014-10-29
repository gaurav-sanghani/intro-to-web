from flask import Flask, render_template, request, make_response, redirect, url_for
app = Flask(__name__)

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
			username=request.cookies.get('username'),
			password=request.cookies.get('password')
		)

@app.route('/logout', methods=['GET'])
def logout():
	resp = redirect(url_for('hello'))
	resp.set_cookie('username', '')
	resp.set_cookie('password', '')

	return resp

if __name__ == '__main__':
	app.run(debug=True)