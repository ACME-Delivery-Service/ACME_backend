select version() as postgresql_version;

CREATE TYPE DHL_location AS ENUM ('EU', 'RU', 'CH', 'UK');

CREATE TYPE DHL_role AS ENUM ('CEO', 'DO', 'CO', 'CS', 'CD');

CREATE TABLE DHL_users (
	user_id SERIAL PRIMARY KEY,
	password BYTEA NOT NULL, /* HASH OF THE PASSWORD IS STORED AS ARRAY OF BYTES */
	name VARCHAR(255) NOT NULL,
	user_location DHL_location NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE login(
	user_id serial PRIMARY KEY,
	last_logged_in TIMESTAMP NOT NULL,
	FOREIGN KEY(user_id) REFERENCES DHL_users(user_id)
);
	
CREATE TABLE user_roles(
	user_id serial,
	role DHL_role,
	PRIMARY KEY(user_id),
	FOREIGN KEY(user_id) REFERENCES DHL_users(user_id)
);