CREATE TABLE Credit (
	credit_id serial NOT NULL,
	user_id integer NOT NULL,
	credit_limit integer NOT NULL,
	duration DATE NOT NULL,
	credit_currency varchar(25) NOT NULL,
	passport_number integer NOT NULL,
	CONSTRAINT Credit_pk PRIMARY KEY (credit_id)
) WITH (
  OIDS=FALSE
);



CREATE TABLE User (
	user_id serial NOT NULL,
	username serial(25) NOT NULL,
	first_name varchar(25) NOT NULL,
	last_name varchar(25) NOT NULL,
	email varchar(25) NOT NULL,
	password varchar(25) NOT NULL,
	phone varchar(25) NOT NULL,
	user_status varchar(25) NOT NULL,
	CONSTRAINT User_pk PRIMARY KEY (user_id)
) WITH (
  OIDS=FALSE
);



CREATE TABLE Payment (
	payment_id serial NOT NULL,
	user_id integer NOT NULL,
	credit_id integer NOT NULL,
	payment integer NOT NULL,
	date DATE NOT NULL,
	CONSTRAINT Payment_pk PRIMARY KEY (payment_id)
) WITH (
  OIDS=FALSE
);



ALTER TABLE Credit ADD CONSTRAINT Credit_fk0 FOREIGN KEY (credit_id) REFERENCES Payment(credit_id);

ALTER TABLE User ADD CONSTRAINT User_fk0 FOREIGN KEY (user_id) REFERENCES Payment(user_id);




