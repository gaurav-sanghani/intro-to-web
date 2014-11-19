import collections
import data
import flask
import functools


class Error(Exception):
	pass


class UserCreationError(Error):
	pass


class UserLoginError(Error):
	pass


User = collections.namedtuple('User', ['username', 'password'])

def current_user():
	cookie = flask.request.cookies
	username = cookie.get('username')
	password = cookie.get('password')
	if username and password:
		return User(username, password)

	return None

def set_current_user(user_data, response):
	response.set_cookie('username', user_data['username'])
	response.set_cookie('password', user_data['password'])

def require_auth(fn):
	@functools.wraps(fn)
	def redirect_to_login(*args, **kwargs):
		user = current_user()
		if not user:
			return flask.redirect(flask.url_for('login'))
		return fn(*args, **kwargs)

	return redirect_to_login


def require_no_auth(fn):
	@functools.wraps(fn)
	def redirect_home(*args, **kwargs):
		user = current_user()
		if user:
			return flask.redirect(flask.url_for('home'))
		return fn(*args, **kwargs)

	return redirect_home


def create_user(response=None):
	if not response:
		response = flask.make_response()

	form_data = flask.request.form
	try:
		data.add_user(
			form_data['username'],
			form_data['password'],
			form_data['first_name'],
			form_data['last_name'],
			form_data['email'],
		)
		
		set_current_user(form_data, response)

		return response
	except Exception as e:
		raise UserCreationError('Unable to create user')


def login_user(response=None):
	if not response:
		response = flask.make_response()

	form_data = flask.request.form
	try:
		data.get_user(
			form_data['username'],
			form_data['password'],
		)
		set_current_user(form_data, response)

		return response
	except (data.BadPassword, data.MissingUser) as e:
		raise UserLoginError('Incorrect username/password')
