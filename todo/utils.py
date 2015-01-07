import sqlalchemy


engine = sqlalchemy.create_engine('postgres://app:app@localhost:5432/postgres', convert_unicode=True)
def execute_query(query, *args, **kwargs):
	return engine.execute(sqlalchemy.sql.expression.text(query), *args, **kwargs)