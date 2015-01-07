import datetime
import sqlalchemy
import utils

utils.execute_query(
	""" CREATE TABLE IF NOT EXISTS public.items (
		id serial primary key,
		username text NOT NULL,
		data text NOT NULL,
		created_ts timestamp without time zone NOT NULL,
		updated_ts timestamp without time zone,
		deleted_ts timestamp without time zone
	);
""")


def add_item(user, data):
	utils.execute_query(
		'''INSERT INTO public.items (username, data, created_ts) VALUES (
				:username,
				:data,
				NOW()
			)
		''',
		username=user.username,
		data=data,
	)

	return True


def get_items(user):
	return utils.execute_query(
		''' SELECT 
				* 
			FROM public.items
			WHERE
				username=:username 
				AND deleted_ts IS NULL
			;
		''',
		username=user.username
	).fetchall()


def update_item(user, item_id, data):
	utils.execute_query(
		''' UPDATE public.items
			SET
				data = :data,
				updated_ts = NOW()
			WHERE 
				id=:item_id
				AND username=:username
				AND deleted_ts IS NULL
		''',
		data=data,
		item_id=item_id,
		username=user.username,
	)

def delete_item(user, item_id):
	utils.execute_query(
		''' UPDATE public.items
			SET
				deleted_ts = NOW()
			WHERE
				id=:item_id
				AND username=:username
				AND deleted_ts IS NULL
		''',
		item_id=item_id,
		username=user.username
	)




