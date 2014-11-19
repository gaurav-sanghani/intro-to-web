import bcrypt
import sqlalchemy


engine = sqlalchemy.create_engine('postgres://app:app@localhost:5432/postgres', convert_unicode=True)
def execute_query(query, *args, **kwargs):
	return engine.execute(sqlalchemy.sql.expression.text(query), *args, **kwargs)


execute_query("""
	CREATE TABLE IF NOT EXISTS public.users (
		username text PRIMARY KEY,
		password text NOT NULL,
		first_name text NOT NULL,
		last_name text NOT NULL,
		email text NOT NULL
	);
""")


class Error(Exception):
	pass


class MissingUser(Error):
	pass


class BadPassword(Error):
	pass


def add_user(username, password, first_name, last_name, email):
	hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
	execute_query(
		'INSERT INTO public.users VALUES (:username, :password, :first_name, :last_name, :email);',
		username=username,
		password=hashed,
		first_name=first_name,
		last_name=last_name,
		email=email
	)
	return True

def get_user(username, password):
	user = execute_query(
		'SELECT * FROM public.users WHERE username=:username',
		username=username
	).fetchone()

	if not user:
		raise MissingUser(username)

	if bcrypt.hashpw(password.encode('utf-8'), user['password'].encode('utf-8')) == user['password']:
		return user
	else:
		raise BadPassword(username)

