CREATE TYPE shape_type AS ENUM ('postcard', 'letter', 'large_envelope', 'parcel');

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

CREATE TABLE acme_customers (
	customer_id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL,
    CONSTRAINT contact_id_fkey
        FOREIGN KEY (contact_id)
        REFERENCES contacts (contact_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE acme_orders (
    order_id serial PRIMARY KEY,
    created_on TIMESTAMP NOT NULL,
    comment TEXT,
    customer_id INTEGER NOT NULL,
    priority INTEGER NOT NULL,
    CONSTRAINT customer_id_fkey
        FOREIGN KEY (customer_id)
        REFERENCES acme_customers (customer_id)
        ON UPDATE NO ACTION ON DELETE RESTRICT
);

CREATE TABLE parcels (
    parcel_id serial PRIMARY KEY,
    weight REAL NOT NULL,
    dimensions REAL[3] NOT NULL,
    shape shape_type NOT NULL,
    order_id INTEGER,
    CONSTRAINT order_id_fkey
        FOREIGN KEY (order_id)
        REFERENCES acme_orders (order_id)
        ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE warehouses (
    warehouse_id serial PRIMARY KEY,
    warehouse_name VARCHAR(255),
    contact_id INTEGER NOT NULL,
    /** Area of warehouse m^2
     */
    max_capacity REAL NOT NULL,
    /** For backward compatibility with old acme_orders
     * in case warehouse shuts down.
     */
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT warehouses_contact_id
        FOREIGN KEY (contact_id)
        REFERENCES contacts (contact_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TYPE order_status_type AS ENUM ('created', 'approved', 'en_rout', 'stored', 'delivered');

CREATE TABLE acme_order_status (
    created_on TIMESTAMP NOT NULL,
    status order_status_type NOT NULL,
    warehouse_id INTEGER /* OPTIONAL */,

    order_id INTEGER NOT NULL,
    CONSTRAINT order_status_pkey
        PRIMARY KEY (order_id, created_on),
    CONSTRAINT order_status_dispatch_order_fkey
        FOREIGN KEY (order_id)
        REFERENCES acme_orders (order_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT order_status_warehouse_id_fkey
        FOREIGN KEY (warehouse_id)
        REFERENCES warehouses (warehouse_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TYPE acme_location AS ENUM ('EU', 'RU', 'CH', 'UK');

CREATE TYPE acme_role AS ENUM ('CEO', 'DO', 'CO', 'CS', 'CD');

CREATE TABLE acme_users (
	user_id SERIAL PRIMARY KEY,
	password BYTEA NOT NULL, /* HASH OF THE PASSWORD IS STORED AS ARRAY OF BYTES */
	user_location acme_location NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
    contact_id INTEGER NOT NULL,
    token VARCHAR(255) UNIQUE,
    file_url VARCHAR(255),
    CONSTRAINT contact_id_fkey
        FOREIGN KEY (contact_id)
        REFERENCES contacts (contact_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
	
CREATE TABLE user_roles(
	user_id serial,
	role acme_role,
	PRIMARY KEY(user_id),
	FOREIGN KEY(user_id) REFERENCES acme_users(user_id)
);

CREATE TYPE delivery_status_type AS ENUM ('pending', 'in_progress', 'completed');

CREATE TABLE locations (
    location_id serial PRIMARY KEY,
    location_address VARCHAR(255),
    lat_long point NOT NULL
);

CREATE TABLE delivery_operators (
    operator_id INTEGER PRIMARY KEY,
    current_pos INTEGER,
    pos_last_updated TIMESTAMP,
    CONSTRAINT acme_user_id_fkey
        FOREIGN KEY (operator_id)
        REFERENCES acme_users (user_id)
        ON UPDATE NO ACTION ON DELETE RESTRICT,
    CONSTRAINT current_pos_id_fkey
        FOREIGN KEY (current_pos)
        REFERENCES locations(location_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

/*** 
Shows the time period at which delivery operator was active
Used to calculate working hours of the delivery operator.
 ***/
CREATE TYPE delivery_period AS (
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

CREATE TABLE order_deliveries (
    order_id INTEGER NOT NULL,
    delivery_operator_id INTEGER NOT NULL,
    delivery_status delivery_status_type NOT NULL,
    start_location_id INTEGER NOT NULL,
    end_location_id INTEGER NOT NULL,
    active_time_periods delivery_period[],
    CONSTRAINT order_id_fkey
        FOREIGN KEY (order_id)
        REFERENCES acme_orders (order_id)
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
        PRIMARY KEY (order_id, delivery_operator_id) 
);

