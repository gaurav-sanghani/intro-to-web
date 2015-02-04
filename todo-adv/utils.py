import sqlalchemy

USERNAME = 'vagrant'
PASSWORD = 'vagrant'
DATABASE = 'vagrant'


engine = sqlalchemy.create_engine(
	'postgres://{username}:{pw}@localhost:5432/{db}'.format(
		username=USERNAME,
		pw=PASSWORD,
		db=DATABASE
	), convert_unicode=True
)
def execute_query(query, *args, **kwargs):
	return engine.execute(sqlalchemy.sql.expression.text(query), *args, **kwargs)