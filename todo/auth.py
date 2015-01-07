import collections
import flask
import functools
import models.user


class Error(Exception):
	pass


class UserCreationError(Error):
	pass


class UserLoginError(Error):
	pass


User = collections.namedtuple('User', ['username'])#, 'password'])

def current_user():
	#cookie = flask.request.cookies
	#password = cookie.get('password')
	username = flask.session.get('username') #cookie.get('username')
	if username: # and password:
		return User(username)#, password)

	return None

def set_current_user(user_data, response):
	#response.set_cookie('username', user_data['username'])
	#response.set_cookie('password', user_data['password'])
	flask.session['username'] = user_data['username']

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
		models.user.add_user(
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
		models.user.get_user(
			form_data['username'],
			form_data['password'],
		)
		set_current_user(form_data, response)

		return response
	except (models.user.BadPassword, models.MissingUser) as e:
		raise UserLoginError('Incorrect username/password')

def logout(response=None):
	if not response:
		response = flask.make_response()

	del flask.session['username']	

	#response.set_cookie(
	#	'username', '',
	#	expires='Thu, 01 Jan 1970 00:00:00 GMT'
	#)
	#response.set_cookie(
	#	'password', '',
	#	expires='Thu, 01 Jan 1970 00:00:00 GMT'
	#)

	return response
