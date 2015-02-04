CREATE TABLE IF NOT EXISTS public.users (
		username text PRIMARY KEY,
		password text NOT NULL,
		first_name text NOT NULL,
		last_name text NOT NULL,
		email text NOT NULL
	);