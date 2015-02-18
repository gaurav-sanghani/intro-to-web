import auth
import flask
import models.items


app = flask.Flask(__name__)


@app.route('/')
@auth.require_auth
def home():
	user = auth.current_user()
	return flask.render_template('index.html',
		username=user.username,
		items=models.items.get_items(user),
		#password=user.password,
	)

@app.route('/items', methods=['POST'])
@auth.require_auth
def items():
	user = auth.current_user()
	if flask.request.method == 'POST':
		# Needed since forms cannot perform PUT/PATCH/DELETE
		true_method = flask.request.args.get('method', '').upper()
		if not true_method:
			models.items.add_item(user, flask.request.form['data'])
		elif true_method == 'PATCH':
			models.items.update_item(
				user,
				flask.request.form['id'],
				flask.request.form['data']
			)
		elif true_method == 'DELETE':
			models.items.delete_item(user, flask.request.form['id'])
		
		return flask.redirect(flask.url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
@auth.require_no_auth
def signup():
	error_message = None
	if flask.request.method == 'POST':
		try:
			resp = flask.redirect(flask.url_for('home'))
			auth.create_user(resp)

			return resp
		except auth.UserCreationError as e:
			error_message = e.message

	return flask.render_template('create.html', message=error_message)


@app.route('/login', methods=['GET', 'POST'])
@auth.require_no_auth
def login():
	error_message = None
	if flask.request.method == 'POST':
		try:
			resp = flask.redirect(flask.url_for('home'))
			auth.login_user(resp)
			return resp
		except auth.UserLoginError as e:
			error_message = e.message

	return flask.render_template(
		'login.html',
		message=error_message
	)


@app.route('/logout', methods=['GET'])
@auth.require_auth
def logout():
	resp = flask.redirect(flask.url_for('home'))
	auth.logout(resp)
	return resp

if __name__ == '__main__':
	app.secret_key = 'abcd'
	app.run(debug=True, host='0.0.0.0')
