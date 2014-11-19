import sqlalchemy
import bcrypt
engine = sqlalchemy.create_engine('postgres://app:app@localhost:5432/postgres', convert_unicode=True)


engine.execute("""
	CREATE TABLE IF NOT EXISTS users (
		username text PRIMARY KEY,
		password text NOT NULL,
		first_name text NOT NULL,
		last_name text NOT NULL,
		email text NOT NULL
	);
""")

def add_user(username, password, first_name, last_name, email):
	hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
	engine.execute(
		'INSERT INTO users VALUES (:username, :password, :first_name, :last_name, :email);',
		{
			'username':username,
			'password':hashed,
			'first_name':first_name,
			'last_name':last_name,
			'email':email 
		}
	)
	return True

def get_user(username, password):
	user = engine.execute(
		'SELECT * FROM users WHERE username=:1',
		[username]
	).fetchall()

	if not user:
		return None

	if bcrypt.hashpw(password.encode('utf-8'), user['password']) == user['password']:
		return user
	else:
		return None

