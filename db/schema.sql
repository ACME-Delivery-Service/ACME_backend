CREATE TYPE shape_type AS ENUM ('postcard', 'letter', 'large_envelope', 'parcel');

CREATE TABLE incoming_orders (
    order_id serial PRIMARY KEY,
    created_on TIMESTAMP NOT NULL,
    priority INTEGER NOT NULL
);

CREATE TABLE parcels (
    parcel_id serial PRIMARY KEY,
    weight REAL NOT NULL,
    volume REAL NOT NULL,
    shape shape_type NOT NULL,
    order_id INTEGER,
    CONSTRAINT incoming_order_id_fkey
        FOREIGN KEY (order_id)
        REFERENCES incoming_orders (order_id)
        ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE dispatch_orders (
    order_id INTEGER PRIMARY KEY,
    CONSTRAINT dispatch_order_incoming_order_id_fkey
        FOREIGN KEY (order_id)
        REFERENCES incoming_orders (order_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE contacts (
    contact_id serial PRIMARY KEY,
    /*** Fields for general information ***/
    address VARCHAR(255),
    phone_number VARCHAR(20) NOT NULL,
    additional_info TEXT,
    /*** Fields for personal information ***/
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    position VARCHAR(255),
    /*** Fields for company information ***/
    company VARCHAR(255)
);

CREATE TABLE warehouses (
    warehouse_id serial PRIMARY KEY,
    warehouse_name VARCHAR(255),
    contact_id INTEGER NOT NULL,
    /** Area of warehouse m^2
     */
    max_capacity REAL NOT NULL,
    /** For backward compatibility with old orders
     * in case warehouse shuts down.
     */
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT warehouses_contact_id
        FOREIGN KEY (contact_id)
        REFERENCES contacts (contact_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TYPE dispatch_status_type AS ENUM ('created', 'approved', 'en_rout', 'stored', 'delivered');

CREATE TABLE dispatch_status (
    created_on TIMESTAMP NOT NULL,
    status dispatch_status_type NOT NULL,
    warehouse_id INTEGER /* OPTIONAL */,

    dispatch_order_id INTEGER NOT NULL,
    CONSTRAINT dispatch_status_pkey
        PRIMARY KEY (dispatch_order_id, created_on),
    CONSTRAINT dispatch_status_dispatch_order_fkey
        FOREIGN KEY (dispatch_order_id)
        REFERENCES dispatch_orders (order_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT dispatch_status_warehouse_id_fkey
        FOREIGN KEY (warehouse_id)
        REFERENCES warehouses (warehouse_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TYPE transport_type AS ENUM ('airplane', 'truck', 'barge');

CREATE TYPE acmee_location AS ENUM ('EU', 'RU', 'CH', 'UK');

CREATE TYPE acmee_role AS ENUM ('CEO', 'DO', 'CO', 'CS', 'CD');

CREATE TABLE acmee_users (
	user_id SERIAL PRIMARY KEY,
	password BYTEA NOT NULL, /* HASH OF THE PASSWORD IS STORED AS ARRAY OF BYTES */
	name VARCHAR(255) NOT NULL,
	user_location acmee_location NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
    contact_id INTEGER NOT NULL,
    token VARCHAR(255),

    CONSTRAINT contact_id_fkey
        FOREIGN KEY (contact_id)
        REFERENCES contacts (contact_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE login(
	user_id INTEGER PRIMARY KEY,
	last_logged_in TIMESTAMP NOT NULL,
	FOREIGN KEY(user_id) REFERENCES acmee_users(user_id)
);
	
CREATE TABLE user_roles(
	user_id serial,
	role acmee_role,
	PRIMARY KEY(user_id),
	FOREIGN KEY(user_id) REFERENCES acmee_users(user_id)
);

CREATE TABLE delivery_operators (
    operator_id serial PRIMARY KEY,
    user_id INTEGER NOT NULL,
    CONSTRAINT acmee_user_id_fkey
        FOREIGN KEY (user_id)
        REFERENCES acmee_users (user_id)
        ON UPDATE NO ACTION ON DELETE RESTRICT
);

CREATE TYPE delivery_status_type AS ENUM ('pending', 'in_progress', 'completed');

CREATE TABLE locations (
    location_id serial PRIMARY KEY,
    location_address VARCHAR(255),
    lat_long point NOT NULL
);

CREATE TABLE order_deliveries (
    dispatch_order_id INTEGER NOT NULL,
    delivery_operator_id INTEGER NOT NULL,
    delivery_status delivery_status_type NOT NULL,
    start_location_id INTEGER NOT NULL,
    end_location_id INTEGER NOT NULL,

    CONSTRAINT dispatch_order_id_fkey
        FOREIGN KEY (dispatch_order_id)
        REFERENCES dispatch_orders (order_id)
        ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT delivery_operator_id_fkey
        FOREIGN KEY (delivery_operator_id)
        REFERENCES delivery_operators (operator_id)
        ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT start_location_id_fkey
        FOREIGN KEY (start_location_id)
        REFERENCES locations (location_id)
        ON UPDATE NO ACTION ON DELETE RESTRICT,
    CONSTRAINT end_location_id_fkey
        FOREIGN KEY (end_location_id)
        REFERENCES locations (location_id)
        ON UPDATE NO ACTION ON DELETE RESTRICT,
    CONSTRAINT order_deliveries_pkey   
        PRIMARY KEY (dispatch_order_id, delivery_operator_id) 
);

